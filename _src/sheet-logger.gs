/**
 * Digital Autonomous — leads spreadsheet logger
 * =============================================
 *
 * Receives a form submission from digitalautonomous.co.uk and writes it to
 * the spreadsheet as a row, then keeps a Dashboard tab up to date.
 *
 * SETUP (about five minutes, once)
 * --------------------------------
 *  1. Go to sheets.new and name the spreadsheet "Digital Autonomous — Leads".
 *  2. Extensions > Apps Script. Delete whatever is there and paste this file in.
 *  3. Save, then Run > setup. Google will ask you to authorise it; do so.
 *     (It will warn the app is unverified — it is your own script, so choose
 *     Advanced > Go to project.) This builds the Leads and Dashboard tabs.
 *  4. Deploy > New deployment > type "Web app".
 *       Execute as:      Me
 *       Who has access:  Anyone
 *     Deploy, then copy the Web app URL (it ends in /exec).
 *  5. Paste that URL into SHEET_ENDPOINT in _src/content.py, then rebuild and
 *     push. Every submission now lands in the sheet.
 *
 * Changing this script later needs Deploy > Manage deployments > edit > New
 * version, otherwise the old code keeps running.
 *
 * WHY "ANYONE" FOR WHO HAS ACCESS
 * -------------------------------
 * "Anyone" here means "no Google sign-in required". It has to be that, because
 * the request comes from a visitor's browser and visitors are not signed into
 * Google. "Anyone with Google Account" would bounce them to a login screen and
 * the submission would fail.
 *
 * It does NOT share the spreadsheet. Callers cannot open it, read it, or run
 * anything except doGet and doPost below. doPost only ever appends one row.
 * The script runs as you ("Execute as: Me"), which is what lets it write to
 * your sheet — so the code, not the caller, decides what happens.
 *
 * The real exposure is that the URL sits in the page source, so a bot could
 * post junk rows. Three things guard against that: a honeypot field, a shared
 * token, and a check that a submission has a name and a way to reply. If spam
 * ever does get through, change SHARED_TOKEN here and in _src/content.py, then
 * redeploy — that alone invalidates every scraped copy of the URL.
 */

// Must match SHEET_TOKEN in _src/content.py. The web app has to accept
// anonymous requests, because a visitor's browser is not signed into Google.
// This turns away anything that finds the URL without also reading the page
// source. It is a doormat, not a lock — see WHY "ANYONE" below.
var SHARED_TOKEN = 'da-wxFZTutTCD56fDUtoue41_YJeMM5OULh';

var SHEET_NAME = 'Leads';
var DASH_NAME = 'Dashboard';

// Column order. Add one here and it appears on the next submission — on a
// sheet that already holds leads too, because ensureSheet calls syncHeader to
// slot the new heading in and shift the existing data across.
//
// A key must match the form field's `name` attribute in _src/build.py.
var COLUMNS = [
  { key: 'received',     label: 'Received',       width: 140 },
  { key: 'name',         label: 'Name',           width: 160 },
  { key: 'email',        label: 'Email',          width: 220 },
  { key: 'phone',        label: 'Phone',          width: 150 },
  { key: 'company',      label: 'Company',        width: 180 },
  { key: 'company_type', label: 'Company type',   width: 200 },
  { key: 'company_size', label: 'Company size',   width: 150 },
  { key: 'goal',         label: 'Wants to improve', width: 190 },
  { key: 'message',      label: 'What they said', width: 320 },
  { key: 'form',         label: 'Came from',      width: 120 },
  { key: 'page',         label: 'Page',           width: 120 },
  { key: 'referrer',     label: 'Referrer',       width: 180 },
  { key: 'status',       label: 'Status',         width: 130 },
  { key: 'followup',     label: 'Follow up on',   width: 120 },
  { key: 'notes',        label: 'Notes',          width: 320 }
];

var STATUSES = ['New', 'Contacted', 'Audit booked', 'Audit done',
                'Proposal sent', 'Won', 'Lost', 'Not a fit'];

var NAVY = '#0a1a3a';
var BLUE = '#00a6fb';


/* ------------------------------------------------------------------ *
 * Receiving a submission
 * ------------------------------------------------------------------ */
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    // 1. A filled honeypot means an automated submission. Answer normally so
    //    the sender learns nothing, but write nothing down.
    if (data.website) return json({ ok: true });

    // 2. Wrong or missing token: not from our forms.
    if (SHARED_TOKEN && data.token !== SHARED_TOKEN) {
      return json({ ok: false, error: 'rejected' });
    }

    // 3. Junk filter: a real enquiry has a name and a way to reply.
    var name = clean(data.name, 120);
    var email = clean(data.email, 160);
    var phone = clean(data.phone, 40);
    if (!name || (!email && !phone)) return json({ ok: false, error: 'incomplete' });
    if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      return json({ ok: false, error: 'bad email' });
    }

    var sheet = ensureSheet();
    var row = COLUMNS.map(function (c) {
      if (c.key === 'received') return new Date();
      if (c.key === 'status') return 'New';
      if (c.key === 'followup' || c.key === 'notes') return '';
      return clean(data[c.key], c.key === 'message' ? 2000 : 300);
    });

    sheet.appendRow(row);
    styleNewRow(sheet, sheet.getLastRow());
    refreshDashboard();

    return json({ ok: true });
  } catch (err) {
    // Record the failure rather than losing it silently.
    try {
      ensureSheet().appendRow([new Date(), 'COULD NOT READ SUBMISSION', String(err),
                               String((e && e.postData ? e.postData.contents : '')).slice(0, 500)]);
    } catch (ignored) {}
    return json({ ok: false, error: String(err) });
  }
}

// Trim, cap the length, and never let a value start a spreadsheet formula.
function clean(v, max) {
  var s = String(v === undefined || v === null ? '' : v).trim().slice(0, max || 300);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

// A browser opening the URL should see something friendly, not an error.
function doGet() {
  return json({ ok: true, message: 'Digital Autonomous lead logger is running.' });
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}


/* ------------------------------------------------------------------ *
 * Sheet setup
 * ------------------------------------------------------------------ */
function setup() {
  ensureSheet();
  refreshDashboard();
  SpreadsheetApp.getActive().toast('Leads and Dashboard are ready.', 'Digital Autonomous', 5);
}

function ensureSheet() {
  var ss = SpreadsheetApp.getActive();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME, 0);

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(COLUMNS.map(function (c) { return c.label; }));
  } else {
    syncHeader(sheet);
  }

  var header = sheet.getRange(1, 1, 1, COLUMNS.length);
  header.setBackground(NAVY).setFontColor('#ffffff').setFontWeight('bold')
        .setVerticalAlignment('middle');
  sheet.setRowHeight(1, 34);
  sheet.setFrozenRows(1);

  COLUMNS.forEach(function (c, i) { sheet.setColumnWidth(i + 1, c.width); });

  // Status column becomes a dropdown you can filter and chart on.
  var statusCol = colIndex('status');
  var rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(STATUSES, true).setAllowInvalid(false).build();
  sheet.getRange(2, statusCol, Math.max(sheet.getMaxRows() - 1, 1), 1).setDataValidation(rule);

  // Won green, Lost grey, anything overdue for follow-up in amber.
  var lastRow = Math.max(sheet.getMaxRows(), 2);
  var body = sheet.getRange(2, 1, lastRow - 1, COLUMNS.length);
  var a1 = columnLetter(statusCol);
  var f1 = columnLetter(colIndex('followup'));
  sheet.setConditionalFormatRules([
    SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=$' + a1 + '2="Won"')
      .setBackground('#e6f7ef').setRanges([body]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=$' + a1 + '2="Lost"')
      .setBackground('#f2f2f2').setFontColor('#888888').setRanges([body]).build(),
    SpreadsheetApp.newConditionalFormatRule()
      .whenFormulaSatisfied('=AND($' + f1 + '2<>"",$' + f1 + '2<TODAY(),$' + a1 + '2<>"Won",$' + a1 + '2<>"Lost")')
      .setBackground('#fff4e0').setRanges([body]).build()
  ]);

  if (!sheet.getFilter()) {
    sheet.getRange(1, 1, Math.max(sheet.getLastRow(), 2), COLUMNS.length).createFilter();
  }
  return sheet;
}

/**
 * Bring a sheet that already has rows in it up to date with COLUMNS.
 *
 * Adding a column used to work only on an empty sheet. A sheet with leads in
 * it kept its original header, so every new submission wrote its values one
 * place to the left of the heading describing them — silently, and only
 * visible once somebody read a row and found the phone number under "Company".
 *
 * This walks COLUMNS in order and inserts any heading the sheet does not have
 * at the position it belongs, pushing existing data right so old rows stay
 * under their own headings. A heading that exists but sits somewhere else is
 * left where it is, and a column you added by hand is never touched — this
 * only ever adds.
 */
function syncHeader(sheet) {
  for (var i = 0; i < COLUMNS.length; i++) {
    var header = sheet.getRange(1, 1, 1, Math.max(sheet.getLastColumn(), 1)).getValues()[0];
    if (header.indexOf(COLUMNS[i].label) > -1) continue;

    if (i < sheet.getMaxColumns()) {
      sheet.insertColumnBefore(i + 1);
    } else {
      sheet.insertColumnAfter(sheet.getMaxColumns());
    }
    sheet.getRange(1, i + 1).setValue(COLUMNS[i].label);
  }
}

function styleNewRow(sheet, row) {
  sheet.getRange(row, colIndex('received')).setNumberFormat('dd/MM/yyyy HH:mm');
  sheet.getRange(row, colIndex('followup')).setNumberFormat('dd/MM/yyyy');
  sheet.getRange(row, 1, 1, COLUMNS.length).setVerticalAlignment('top').setWrap(true);
}

function colIndex(key) {
  for (var i = 0; i < COLUMNS.length; i++) if (COLUMNS[i].key === key) return i + 1;
  return 1;
}

function columnLetter(n) {
  var s = '';
  while (n > 0) { var m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = (n - m - 1) / 26; }
  return s;
}


/* ------------------------------------------------------------------ *
 * Dashboard — formulas, so it stays live as you edit the Leads tab
 * ------------------------------------------------------------------ */
function refreshDashboard() {
  var ss = SpreadsheetApp.getActive();
  var dash = ss.getSheetByName(DASH_NAME);
  if (!dash) dash = ss.insertSheet(DASH_NAME, 1);
  dash.clear();

  var L = "'" + SHEET_NAME + "'!";
  var received = L + columnLetter(colIndex('received')) + '2:' + columnLetter(colIndex('received'));
  var status   = L + columnLetter(colIndex('status'))   + '2:' + columnLetter(colIndex('status'));
  var type     = L + columnLetter(colIndex('company_type')) + '2:' + columnLetter(colIndex('company_type'));
  var size     = L + columnLetter(colIndex('company_size')) + '2:' + columnLetter(colIndex('company_size'));
  var goal     = L + columnLetter(colIndex('goal'))     + '2:' + columnLetter(colIndex('goal'));
  var form     = L + columnLetter(colIndex('form'))     + '2:' + columnLetter(colIndex('form'));
  var followup = L + columnLetter(colIndex('followup')) + '2:' + columnLetter(colIndex('followup'));

  dash.getRange('A1').setValue('Digital Autonomous — leads at a glance');
  dash.getRange('A1').setFontSize(16).setFontWeight('bold').setFontColor(NAVY);
  dash.getRange('A2').setFormula('="Updated "&TEXT(NOW(),"dd/MM/yyyy HH:mm")');
  dash.getRange('A2').setFontColor('#777777');

  var tiles = [
    ['Total leads',      '=COUNTA(' + received + ')'],
    ['New, not yet contacted', '=COUNTIF(' + status + ',"New")'],
    ['Last 7 days',      '=COUNTIFS(' + received + ',">="&TODAY()-7)'],
    ['Last 30 days',     '=COUNTIFS(' + received + ',">="&TODAY()-30)'],
    ['Audits booked',    '=COUNTIF(' + status + ',"Audit booked")'],
    ['Won',              '=COUNTIF(' + status + ',"Won")'],
    ['Follow-ups overdue', '=COUNTIFS(' + followup + ',"<"&TODAY(),' + followup + ',"<>",' +
                            status + ',"<>Won",' + status + ',"<>Lost")']
  ];
  dash.getRange('A4').setValue('Overview').setFontWeight('bold').setFontColor(NAVY);
  tiles.forEach(function (t, i) {
    var r = 5 + i;
    dash.getRange(r, 1).setValue(t[0]);
    dash.getRange(r, 2).setFormula(t[1]).setFontWeight('bold').setHorizontalAlignment('left');
  });
  dash.getRange(5, 1, tiles.length, 2).setBorder(true, true, true, true, true, true, '#e0e0e0',
                                                 SpreadsheetApp.BorderStyle.SOLID);

  dash.getRange('D4').setValue('By status').setFontWeight('bold').setFontColor(NAVY);
  STATUSES.forEach(function (st, i) {
    dash.getRange(5 + i, 4).setValue(st);
    dash.getRange(5 + i, 5).setFormula('=COUNTIF(' + status + ',"' + st + '")');
  });

  dash.getRange('G4').setValue('By company type').setFontWeight('bold').setFontColor(NAVY);
  dash.getRange('G5').setFormula(
    '=IFERROR(QUERY(' + type + ',"select Col1, count(Col1) where Col1 is not null ' +
    'group by Col1 order by count(Col1) desc label count(Col1) \'\'",0),"No leads yet")');

  dash.getRange('J4').setValue('By source').setFontWeight('bold').setFontColor(NAVY);
  dash.getRange('J5').setFormula(
    '=IFERROR(QUERY(' + form + ',"select Col1, count(Col1) where Col1 is not null ' +
    'group by Col1 order by count(Col1) desc label count(Col1) \'\'",0),"No leads yet")');

  // The two qualifying answers. Size says whether the work is worth building;
  // the goal says which service to open the audit with.
  dash.getRange('M4').setValue('By company size').setFontWeight('bold').setFontColor(NAVY);
  dash.getRange('M5').setFormula(
    '=IFERROR(QUERY(' + size + ',"select Col1, count(Col1) where Col1 is not null ' +
    'group by Col1 order by count(Col1) desc label count(Col1) \'\'",0),"No leads yet")');

  dash.getRange('P4').setValue('What they want to improve').setFontWeight('bold').setFontColor(NAVY);
  dash.getRange('P5').setFormula(
    '=IFERROR(QUERY(' + goal + ',"select Col1, count(Col1) where Col1 is not null ' +
    'group by Col1 order by count(Col1) desc label count(Col1) \'\'",0),"No leads yet")');

  // Sits below the panels above, which grow downwards as more distinct
  // answers arrive — a QUERY that runs into another one returns #REF and
  // takes the whole dashboard with it.
  dash.getRange('A25').setValue('Needs attention').setFontWeight('bold').setFontColor(NAVY);
  dash.getRange('A26').setFormula(
    '=IFERROR(QUERY(' + L + 'A2:' + columnLetter(COLUMNS.length) + ',"select ' +
    columnLetter(colIndex('received')) + ', ' + columnLetter(colIndex('name')) + ', ' +
    columnLetter(colIndex('company')) + ', ' + columnLetter(colIndex('company_size')) + ', ' +
    columnLetter(colIndex('goal')) + ', ' + columnLetter(colIndex('phone')) + ', ' +
    columnLetter(colIndex('status')) + ' where ' + columnLetter(colIndex('status')) +
    " = 'New' order by " + columnLetter(colIndex('received')) +
    ' desc limit 15",0),"Nothing waiting — all caught up.")');

  [1, 4, 7, 10, 13, 16].forEach(function (c) { dash.setColumnWidth(c, 190); });
  [2, 5, 8, 11, 14, 17].forEach(function (c) { dash.setColumnWidth(c, 90); });
  dash.setHiddenGridlines(true);
}


/* ------------------------------------------------------------------ *
 * Optional: a Monday morning summary by email.
 * Triggers > Add trigger > weeklyDigest > Time-driven > Week timer.
 * ------------------------------------------------------------------ */
function weeklyDigest() {
  var sheet = SpreadsheetApp.getActive().getSheetByName(SHEET_NAME);
  if (!sheet || sheet.getLastRow() < 2) return;

  var rows = sheet.getRange(2, 1, sheet.getLastRow() - 1, COLUMNS.length).getValues();
  var cutoff = new Date(); cutoff.setDate(cutoff.getDate() - 7);

  var recent = rows.filter(function (r) { return r[colIndex('received') - 1] >= cutoff; });
  var open = rows.filter(function (r) { return r[colIndex('status') - 1] === 'New'; });

  var body = 'Last 7 days: ' + recent.length + ' new lead(s).\n' +
             'Waiting on you: ' + open.length + '\n\n';
  recent.forEach(function (r) {
    body += '• ' + r[colIndex('name') - 1] + ' — ' + r[colIndex('company_type') - 1] +
            ', ' + r[colIndex('company_size') - 1] +
            '\n    wants to ' + String(r[colIndex('goal') - 1] || 'unknown').toLowerCase() +
            ' — ' + r[colIndex('phone') - 1] + '\n';
  });
  body += '\n' + SpreadsheetApp.getActive().getUrl();

  MailApp.sendEmail(Session.getEffectiveUser().getEmail(),
                    'Leads this week: ' + recent.length, body);
}

/* ------------------------------------------------------------------ *
 * Maintenance menu
 *
 * Adds a "Digital Autonomous" menu to the spreadsheet. Deliberately not
 * reachable from the web: deleting is done by a signed-in person from
 * inside the sheet, never by anything that has the endpoint URL.
 * ------------------------------------------------------------------ */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Digital Autonomous')
    .addItem('Clear test rows', 'clearTestRows')
    .addSeparator()
    .addItem('Delete ALL leads', 'clearAllLeads')
    .addItem('Rebuild dashboard', 'refreshDashboard')
    .addToUi();
}

// Anything written while setting the sheet up, rather than by a real visitor.
var TEST_MARKERS = /^(TEST|GUARD TEST|GuardTest|Intruder|Bot|Sam$|COULD NOT READ SUBMISSION)/i;

function clearTestRows() {
  var sheet = SpreadsheetApp.getActive().getSheetByName(SHEET_NAME);
  var ui = SpreadsheetApp.getUi();
  if (!sheet || sheet.getLastRow() < 2) { ui.alert('Nothing to clear.'); return; }

  var nameCol = colIndex('name');
  var emailCol = colIndex('email');
  var values = sheet.getRange(2, 1, sheet.getLastRow() - 1, COLUMNS.length).getValues();

  var doomed = [];
  values.forEach(function (r, i) {
    var name = String(r[nameCol - 1] || '').trim();
    var email = String(r[emailCol - 1] || '').trim();
    var blank = !name && !email;
    if (blank || TEST_MARKERS.test(name) || email === 'setup-check@digitalautonomous.co.uk' ||
        email === 'a@b.co' || email === 'nope') {
      doomed.push(i + 2);                      // sheet row number
    }
  });

  if (!doomed.length) { ui.alert('No test rows found — everything here looks like a real lead.'); return; }

  var preview = doomed.slice(0, 10).map(function (rowNum) {
    var r = values[rowNum - 2];
    return '  • row ' + rowNum + ': ' + (String(r[nameCol - 1] || '(no name)')).slice(0, 50);
  }).join('\n');

  var answer = ui.alert('Clear ' + doomed.length + ' test row(s)?',
    preview + (doomed.length > 10 ? '\n  … and ' + (doomed.length - 10) + ' more' : '') +
    '\n\nThis cannot be undone.', ui.ButtonSet.YES_NO);
  if (answer !== ui.Button.YES) return;

  // Delete from the bottom up so earlier row numbers stay valid.
  doomed.sort(function (a, b) { return b - a; })
        .forEach(function (rowNum) { sheet.deleteRow(rowNum); });

  refreshDashboard();
  ui.alert('Removed ' + doomed.length + ' test row(s). ' +
           Math.max(sheet.getLastRow() - 1, 0) + ' lead(s) remain.');
}

function clearAllLeads() {
  var sheet = SpreadsheetApp.getActive().getSheetByName(SHEET_NAME);
  var ui = SpreadsheetApp.getUi();
  if (!sheet || sheet.getLastRow() < 2) { ui.alert('The sheet is already empty.'); return; }

  var count = sheet.getLastRow() - 1;
  var answer = ui.alert('Delete all ' + count + ' row(s)?',
    'Every lead in this sheet will be removed. This cannot be undone.', ui.ButtonSet.YES_NO);
  if (answer !== ui.Button.YES) return;

  sheet.deleteRows(2, count);
  refreshDashboard();
  ui.alert('Sheet cleared. The next row will be a real lead.');
}

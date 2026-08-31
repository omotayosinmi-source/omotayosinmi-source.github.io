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

// Dashboard palette and grid. The brand's two typefaces are both available in
// Sheets, so the tab looks like it belongs to the same company as the website.
var TILE_BG = '#f2f6fb';   // tile fill, a navy-tinted off-white
var RULE    = '#d7e0ec';   // hairlines
var MUTED   = '#66768c';   // captions and small print
var BAND    = '#f7f9fc';   // alternating table rows
var HEAD_F  = 'Montserrat';
var BODY_F  = 'Lato';

// Four columns of content, each a wide value column and a narrower number
// column, with a third column between them. The gutters are not wasted: the
// follow-up table below runs across all of them, which is why every column is
// wide enough to hold a real value rather than being a 20px spacer.
var UNITS = [1, 4, 7, 10];
var GRID  = 11;            // A..K


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

    // The lead is already saved by this point. The dashboard is a view of it,
    // so a fault in drawing one must never be reported to the visitor as a
    // failed submission — they would see the form break and send it again,
    // and the row would be sitting in the sheet the whole time.
    try {
      refreshDashboard();
    } catch (dashErr) {
      console.error('Dashboard rebuild failed: ' + dashErr);
    }

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
 *
 * Everything below sits on the UNITS grid: four columns of content, each
 * a wide value column with a number column beside it. Tiles and
 * breakdown panels share that grid, so the eye runs straight down the
 * page instead of hunting for where the next block starts.
 * ------------------------------------------------------------------ */
function refreshDashboard() {
  var ss = SpreadsheetApp.getActive();
  var dash = ss.getSheetByName(DASH_NAME);
  if (!dash) dash = ss.insertSheet(DASH_NAME, 1);

  // clear() drops content and formatting but leaves merges and conditional
  // rules behind, and merging over a merge that is still there throws. Undo
  // all three, or the second rebuild fails where the first one worked.
  dash.getRange(1, 1, dash.getMaxRows(), dash.getMaxColumns()).breakApart();
  dash.setConditionalFormatRules([]);
  dash.clear();
  if (dash.getMaxColumns() < GRID) {
    dash.insertColumnsAfter(dash.getMaxColumns(), GRID - dash.getMaxColumns());
  }

  var L = "'" + SHEET_NAME + "'!";
  function whole(key) {
    var a = columnLetter(colIndex(key));
    return L + a + '2:' + a;
  }
  var received = whole('received');
  var status   = whole('status');
  var type     = whole('company_type');
  var size     = whole('company_size');
  var goal     = whole('goal');
  var form     = whole('form');
  var followup = whole('followup');

  /* -- masthead ---------------------------------------------------- */
  dash.getRange(1, 1, 1, GRID).merge()
      .setValue('  Digital Autonomous — leads')
      .setBackground(NAVY).setFontColor('#ffffff')
      .setFontFamily(HEAD_F).setFontSize(17).setFontWeight('bold')
      .setVerticalAlignment('middle');
  dash.setRowHeight(1, 54);

  dash.getRange(2, 1, 1, GRID).merge()
      .setFormula('="  Updated "&TEXT(NOW(),"dddd d mmmm yyyy")&" at "&TEXT(NOW(),"HH:mm")')
      .setFontFamily(BODY_F).setFontSize(10).setFontColor(MUTED)
      .setVerticalAlignment('middle');
  dash.setRowHeight(2, 24);
  dash.setRowHeight(3, 12);

  /* -- tiles ------------------------------------------------------- *
   * Seven numbers, four to a band. Workload and outcome lead, because
   * those are the ones that change what you do this morning.          */
  var tiles = [
    ['Total leads',        '=COUNTA(' + received + ')'],
    ['Not yet contacted',  '=COUNTIF(' + status + ',"New")'],
    ['Follow-ups overdue', '=COUNTIFS(' + followup + ',"<"&TODAY(),' + followup + ',"<>",' +
                             status + ',"<>Won",' + status + ',"<>Lost")'],
    ['Audits booked',      '=COUNTIF(' + status + ',"Audit booked")'],
    ['Won',                '=COUNTIF(' + status + ',"Won")'],
    ['Last 7 days',        '=COUNTIFS(' + received + ',">="&TODAY()-7)'],
    ['Last 30 days',       '=COUNTIFS(' + received + ',">="&TODAY()-30)']
  ];

  tiles.forEach(function (t, i) {
    var band = Math.floor(i / UNITS.length);
    drawTile(dash, 4 + band * 3, UNITS[i % UNITS.length], t[0], t[1]);
  });

  /* -- who to call next -------------------------------------------- *
   * Above the breakdowns on purpose: this is the part you act on. The
   * QUERY is capped at 15 rows, so what sits below it never moves.    */
  var CALL = 10;
  sectionHeading(dash, CALL, 'Who to call next');

  var heads = ['Name', 'Came in', 'Company', 'Wants to improve', 'Size', 'Phone', 'Status'];
  dash.getRange(CALL + 1, 1, 1, heads.length).setValues([heads])
      .setBackground(NAVY).setFontColor('#ffffff').setFontWeight('bold')
      .setFontFamily(BODY_F).setFontSize(10).setVerticalAlignment('middle');
  dash.setRowHeight(CALL + 1, 30);

  dash.getRange(CALL + 2, 1).setFormula(
    '=IFERROR(QUERY(' + L + 'A2:' + columnLetter(COLUMNS.length) + ',"select ' +
    columnLetter(colIndex('name')) + ', ' + columnLetter(colIndex('received')) + ', ' +
    columnLetter(colIndex('company')) + ', ' + columnLetter(colIndex('goal')) + ', ' +
    columnLetter(colIndex('company_size')) + ', ' + columnLetter(colIndex('phone')) + ', ' +
    columnLetter(colIndex('status')) + ' where ' + columnLetter(colIndex('status')) +
    " = 'New' order by " + columnLetter(colIndex('received')) +
    ' desc limit 15",0),"Nothing waiting — all caught up.")');

  dash.getRange(CALL + 2, 1, 15, heads.length)
      .setFontFamily(BODY_F).setFontSize(10).setVerticalAlignment('middle');
  dash.getRange(CALL + 2, 2, 15, 1).setNumberFormat('dd/MM/yyyy HH:mm');
  for (var r = CALL + 2; r < CALL + 17; r++) dash.setRowHeight(r, 24);

  /* -- the mix ------------------------------------------------------ */
  var MIX = CALL + 18;
  sectionHeading(dash, MIX, 'The mix');

  function byQuery(range) {
    return '=IFERROR(QUERY(' + range + ',"select Col1, count(Col1) where Col1 is not null ' +
           'group by Col1 order by count(Col1) desc label count(Col1) \'\'",0),"No leads yet")';
  }

  // The row counts are the most answers each question can produce: five sizes,
  // four goals, the status list, and a handful of forms. The band below starts
  // clear of the tallest of them.
  [['By company size', size, 5], ['What they want to improve', goal, 4],
   ['By status', status, STATUSES.length], ['By source', form, 4]
  ].forEach(function (p, i) {
    drawPanel(dash, MIX + 1, UNITS[i], p[0], byQuery(p[1]), p[2]);
  });

  // Company type has by far the most possible answers, so it gets a band to
  // itself and room to grow downwards without running into anything.
  drawPanel(dash, MIX + 12, UNITS[0], 'By company type', byQuery(type), 20);

  /* -- grid, banding, chrome --------------------------------------- */
  [1, 4, 7, 10].forEach(function (c) { dash.setColumnWidth(c, 170); });
  [2, 5, 8, 11].forEach(function (c) { dash.setColumnWidth(c, 115); });
  [3, 6, 9].forEach(function (c) { dash.setColumnWidth(c, 145); });

  dash.setConditionalFormatRules([
    SpreadsheetApp.newConditionalFormatRule()
      .whenFormulaSatisfied('=AND(ISEVEN(ROW()),$A' + (CALL + 2) + '<>"")')
      .setBackground(BAND)
      .setRanges([dash.getRange(CALL + 2, 1, 15, heads.length)])
      .build()
  ]);

  dash.setHiddenGridlines(true);
}


/** One number, big, with its caption above it. */
function drawTile(dash, top, col, label, formula) {
  dash.getRange(top, col, 2, 2)
      .setBackground(TILE_BG)
      .setBorder(true, true, true, true, false, false, RULE, SpreadsheetApp.BorderStyle.SOLID);

  dash.getRange(top, col, 1, 2).merge()
      .setValue('  ' + label)
      .setFontFamily(BODY_F).setFontSize(9).setFontColor(MUTED)
      .setVerticalAlignment('middle');

  dash.getRange(top + 1, col, 1, 2).merge()
      .setFormula(formula).setNumberFormat('0')
      .setFontFamily(HEAD_F).setFontSize(21).setFontWeight('bold').setFontColor(NAVY)
      .setVerticalAlignment('top');

  dash.setRowHeight(top, 22);
  dash.setRowHeight(top + 1, 40);
}


/** A section rule: small navy capitals with a hairline under them. */
function sectionHeading(dash, row, text) {
  dash.getRange(row, 1, 1, GRID).merge()
      .setValue(text.toUpperCase())
      .setFontFamily(HEAD_F).setFontSize(10).setFontWeight('bold').setFontColor(NAVY)
      .setVerticalAlignment('bottom')
      .setBorder(null, null, true, null, null, null, NAVY, SpreadsheetApp.BorderStyle.SOLID);
  dash.setRowHeight(row, 30);
}


/**
 * A breakdown: heading, hairline, then a live QUERY underneath.
 *
 * `rows` is how far down the formatting reaches, and must be at least as many
 * answers as the question can have. Formatting further than that is not
 * cosmetic sloppiness — it would run into whatever panel is drawn below and
 * fight it for the same cells.
 */
function drawPanel(dash, row, col, title, formula, rows) {
  dash.getRange(row, col, 1, 2).merge()
      .setValue(title)
      .setFontFamily(BODY_F).setFontSize(10).setFontWeight('bold').setFontColor(NAVY)
      .setVerticalAlignment('middle')
      .setBorder(null, null, true, null, null, null, RULE, SpreadsheetApp.BorderStyle.SOLID);
  dash.setRowHeight(row, 26);

  dash.getRange(row + 1, col).setFormula(formula);
  dash.getRange(row + 1, col, rows, 2)
      .setFontFamily(BODY_F).setFontSize(10).setVerticalAlignment('middle');
  dash.getRange(row + 1, col + 1, rows, 1)
      .setFontWeight('bold').setFontColor(NAVY).setHorizontalAlignment('left');
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

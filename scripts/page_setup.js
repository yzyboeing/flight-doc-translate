'use strict';

const JSZip = require('jszip');
const {
  AlignmentType,
  BorderStyle,
  Footer,
  PageNumber,
  Paragraph,
  Table,
  TableCell,
  TableOfContents,
  TableRow,
  TextRun,
  VerticalAlign,
  WidthType,
} = require('docx');

const MM_TO_TWIP = 56.6929133858;
const mm = (value) => Math.round(value * MM_TO_TWIP);
const LATIN_FONT = { ascii: 'Times New Roman', hAnsi: 'Times New Roman', eastAsia: 'Times New Roman' };
const CJK_NAME = process.env.FLIGHT_DOC_SERIF_CJK || 'Songti SC';
const CJK_FONT = { ascii: CJK_NAME, hAnsi: CJK_NAME, eastAsia: CJK_NAME };
const CJK_CHAR = /[\u3000-\u303F\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\uFF00-\uFFEF]/;
const REVIEW_STATUS = '未经技术复核；不得作为运行依据';

function textRuns(text, options = {}) {
  const source = String(text ?? '');
  if (!source) return [new TextRun({ text: '', ...options, font: LATIN_FONT })];
  const result = [];
  let current = '';
  let currentCjk = CJK_CHAR.test(source[0]);
  for (const character of source) {
    const cjk = CJK_CHAR.test(character);
    if (current && cjk !== currentCjk) {
      result.push(new TextRun({ text: current, ...options, font: currentCjk ? CJK_FONT : LATIN_FONT }));
      current = '';
    }
    current += character;
    currentCjk = cjk;
  }
  if (current) result.push(new TextRun({ text: current, ...options, font: currentCjk ? CJK_FONT : LATIN_FONT }));
  return result;
}

function pageProps({ paper = 'A4', printing = true, landscape = false } = {}) {
  const normalized = String(paper).toUpperCase();
  if (!['A4', 'LETTER'].includes(normalized)) {
    throw new Error(`Unsupported paper size: ${paper}`);
  }

  let width = normalized === 'A4' ? mm(210) : 12240;
  let height = normalized === 'A4' ? mm(297) : 15840;
  if (landscape) [width, height] = [height, width];

  const margin = printing
    ? { top: mm(18), right: mm(16), bottom: mm(18), left: mm(21), header: mm(8), footer: mm(9), gutter: mm(5) }
    : { top: mm(18), right: mm(18), bottom: mm(18), left: mm(18), header: mm(8), footer: mm(9), gutter: 0 };

  return { page: { size: { width, height }, margin } };
}

function buildFooter(documentNumber, status = REVIEW_STATUS) {
  const prefix = documentNumber ? `${documentNumber} ｜ ` : '';
  return new Footer({
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 0 },
        children: [
          ...textRuns(`${prefix}${status} ｜ 第 `, { size: 16 }),
          new TextRun({ children: [PageNumber.CURRENT], font: LATIN_FONT, size: 16 }),
          ...textRuns(' 页 共 ', { size: 16 }),
          new TextRun({ children: [PageNumber.TOTAL_PAGES], font: LATIN_FONT, size: 16 }),
          ...textRuns(' 页', { size: 16 }),
        ],
      }),
    ],
  });
}

function reviewBanner(text = '未经技术复核，不得作为运行依据') {
  const border = { style: BorderStyle.SINGLE, size: 8, color: '000000' };
  return new Table({
    width: { size: 9300, type: WidthType.DXA },
    columnWidths: [9300],
    rows: [
      new TableRow({
        cantSplit: true,
        children: [
          new TableCell({
            width: { size: 9300, type: WidthType.DXA },
            verticalAlign: VerticalAlign.CENTER,
            margins: { top: 120, bottom: 120, left: 160, right: 160 },
            borders: { top: border, bottom: border, start: border, end: border },
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                spacing: { before: 0, after: 0 },
                children: textRuns(text, { bold: true, size: 24 }),
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

function versionBlock(entries) {
  const rows = Array.isArray(entries)
    ? entries
    : Object.entries(entries || {});
  if (!rows.length) throw new Error('versionBlock requires at least one entry');

  const border = { style: BorderStyle.SINGLE, size: 4, color: '000000' };
  const makeCell = (text, width, bold = false) => new TableCell({
    width: { size: width, type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    borders: { top: border, bottom: border, start: border, end: border },
    children: [new Paragraph({
      spacing: { before: 0, after: 0 },
      children: textRuns(String(text ?? ''), { bold, size: 18 }),
    })],
  });

  return new Table({
    width: { size: 9300, type: WidthType.DXA },
    columnWidths: [2600, 6700],
    rows: rows.map(([label, value]) => new TableRow({
      cantSplit: true,
      children: [makeCell(label, 2600, true), makeCell(value, 6700)],
    })),
  });
}

function toc(title = '目录') {
  return [
    new Paragraph({
      pageBreakBefore: true,
      keepNext: true,
      spacing: { before: 0, after: 120 },
      children: textRuns(title, { bold: true, size: 28 }),
    }),
    new TableOfContents(title, { hyperlink: true, headingStyleRange: '1-3' }),
  ];
}

function documentOptions() {
  return { updateFields: true };
}

async function patchMirrorMargins(buffer) {
  const zip = await JSZip.loadAsync(buffer);
  const settingsFile = zip.file('word/settings.xml');
  if (!settingsFile) throw new Error('DOCX is missing word/settings.xml');
  let xml = await settingsFile.async('string');
  if (!/<w:mirrorMargins\b/.test(xml)) {
    if (!xml.includes('</w:settings>')) throw new Error('Unexpected settings.xml structure');
    xml = xml.replace('</w:settings>', '<w:mirrorMargins/></w:settings>');
    zip.file('word/settings.xml', xml);
  }
  return zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' });
}

module.exports = {
  REVIEW_STATUS,
  buildFooter,
  documentOptions,
  mm,
  pageProps,
  patchMirrorMargins,
  reviewBanner,
  toc,
  versionBlock,
};

'use strict';

const {
  AlignmentType,
  BorderStyle,
  ImageRun,
  Paragraph,
  ShadingType,
  Table,
  TableCell,
  TableRow,
  TextRun,
  VerticalAlign,
  WidthType,
} = require('docx');

const fontMap = (latin, cjk) => ({
  latin: { ascii: latin, hAnsi: latin, eastAsia: latin },
  cjk: { ascii: cjk, hAnsi: cjk, eastAsia: cjk },
});
const BODY_FONTS = fontMap('Times New Roman', process.env.FLIGHT_DOC_SERIF_CJK || 'Songti SC');
const COLOR_FONTS = fontMap('Segoe UI', process.env.FLIGHT_DOC_SANS_CJK || 'Hiragino Sans GB');
const CJK_CHAR = /[\u3000-\u303F\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\uFF00-\uFFEF]/;

function cleanHex(value, label) {
  const normalized = String(value || '').replace(/^#/, '').toUpperCase();
  if (!/^[0-9A-F]{6}$/.test(normalized)) throw new Error(`${label} must be a 6-digit hex color`);
  return normalized;
}

function createStyleSet({ color = false, primary = '000000', secondary = '000000' } = {}) {
  primary = cleanHex(primary, 'primary');
  secondary = cleanHex(secondary, 'secondary');
  const fonts = color ? COLOR_FONTS : BODY_FONTS;
  const border = { style: BorderStyle.SINGLE, size: 4, color: '000000' };

  const makeRun = (text, options = {}, selectedFont = fonts.latin) => new TextRun({
    text: String(text ?? ''),
    font: selectedFont,
    size: options.size ?? 21,
    bold: options.bold,
    italics: options.italics,
    color: options.color,
  });

  const splitRuns = (text, options = {}) => {
    const source = String(text ?? '');
    if (!source) return [makeRun('', options)];
    const groups = [];
    let current = '';
    let currentCjk = CJK_CHAR.test(source[0]);
    for (const character of source) {
      const cjk = CJK_CHAR.test(character);
      if (current && cjk !== currentCjk) {
        groups.push(makeRun(current, options, currentCjk ? fonts.cjk : fonts.latin));
        current = '';
      }
      current += character;
      currentCjk = cjk;
    }
    if (current) groups.push(makeRun(current, options, currentCjk ? fonts.cjk : fonts.latin));
    return groups;
  };

  const run = (text, options = {}) => makeRun(text, options, CJK_CHAR.test(String(text ?? '')[0] || '') ? fonts.cjk : fonts.latin);

  const childrenFor = (content, options = {}) => {
    if (Array.isArray(content)) return content;
    if (content instanceof TextRun) return [content];
    return splitRuns(content, options);
  };

  const p = (content, options = {}) => new Paragraph({
    alignment: options.alignment,
    keepNext: options.keepNext,
    keepLines: options.keepLines,
    pageBreakBefore: options.pageBreakBefore,
    indent: options.indent,
    spacing: {
      before: options.before ?? 0,
      after: options.after ?? 80,
      line: options.line ?? 300,
    },
    children: childrenFor(content, options),
  });

  const bullet = (content, level, options = {}) => new Paragraph({
    bullet: { level },
    keepLines: true,
    spacing: { before: 0, after: options.after ?? 40, line: options.line ?? 290 },
    children: childrenFor(content, options),
  });

  const heading = (content, level, options = {}) => new Paragraph({
    heading: level === 2 ? 'Heading2' : 'Heading3',
    keepNext: true,
    pageBreakBefore: options.pageBreakBefore,
    spacing: {
      before: options.before ?? (level === 2 ? 180 : 120),
      after: options.after ?? 70,
    },
    children: splitRuns(content, {
      size: options.size ?? (level === 2 ? 28 : 24),
      bold: true,
      color: color ? primary : '000000',
    }),
  });

  const cell = (content, options = {}) => {
    const paragraphs = Array.isArray(content) && content.every((item) => item instanceof Paragraph)
      ? content
      : [p(content, { after: 0, line: 270, bold: options.bold, alignment: options.alignment })];
    const cellOptions = {
      children: paragraphs,
      verticalAlign: VerticalAlign.CENTER,
      margins: { top: 90, bottom: 90, left: 120, right: 120 },
      borders: { top: border, bottom: border, start: border, end: border },
    };
    if (options.width) cellOptions.width = { size: options.width, type: WidthType.DXA };
    if (options.fill) cellOptions.shading = { type: ShadingType.CLEAR, fill: cleanHex(options.fill, 'fill') };
    if (options.columnSpan) cellOptions.columnSpan = options.columnSpan;
    return new TableCell(cellOptions);
  };

  const figure = (data, options = {}) => {
    const width = options.width;
    const height = options.height;
    if (!(width > 0 && height > 0)) throw new Error('figure requires positive width and height in pixels');
    return new Paragraph({
      alignment: options.alignment || AlignmentType.CENTER,
      keepNext: true,
      spacing: { before: options.before ?? 80, after: options.after ?? 40 },
      children: [new ImageRun({
        type: options.type || 'png',
        data,
        transformation: { width, height },
        altText: {
          title: options.altText || '原文插图',
          description: options.altText || '原文插图',
          name: options.altText || '原文插图',
        },
      })],
    });
  };

  const figCap = (content, options = {}) => new Paragraph({
    alignment: options.alignment || AlignmentType.CENTER,
    keepNext: true,
    keepLines: true,
    spacing: { before: 0, after: 60 },
    children: [run(content, { size: options.size ?? 18, bold: options.bold })],
  });

  const keyTable = (rows, options = {}) => {
    if (!Array.isArray(rows) || !rows.length) throw new Error('keyTable requires at least one English-Chinese row');
    const normalized = rows.map((item, index) => {
      if (Array.isArray(item) && item.length === 2) return item;
      if (item && typeof item === 'object' && 'english' in item && 'chinese' in item) return [item.english, item.chinese];
      throw new Error(`keyTable row ${index + 1} must contain exactly English and Chinese`);
    });
    const widths = options.columnWidths || [3600, 5700];
    if (!Array.isArray(widths) || widths.length !== 2) throw new Error('keyTable must have exactly two column widths');

    const tableRows = [
      new TableRow({
        tableHeader: true,
        cantSplit: true,
        children: [cell('英文', { bold: true, width: widths[0] }), cell('中文', { bold: true, width: widths[1] })],
      }),
      ...normalized.map(([english, chinese]) => new TableRow({
        cantSplit: true,
        children: [cell(english, { width: widths[0] }), cell(chinese, { width: widths[1] })],
      })),
    ];

    return new Table({
      width: { size: widths[0] + widths[1], type: WidthType.DXA },
      columnWidths: widths,
      rows: tableRows,
    });
  };

  const gap = (twips = 100) => new Paragraph({ spacing: { before: 0, after: twips }, children: [] });
  const rule = () => new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: color ? secondary : '000000' } },
    spacing: { before: 40, after: 80 },
    children: [],
  });

  return {
    palette: { primary, secondary },
    p,
    b1: (content, options) => bullet(content, 0, options),
    b2: (content, options) => bullet(content, 1, options),
    h2: (content, options) => heading(content, 2, options),
    h3: (content, options) => heading(content, 3, options),
    note: (content, options = {}) => p(content, { ...options, size: options.size ?? 17, italics: options.italics ?? true }),
    cell,
    figure,
    figCap,
    keyTable,
    gap,
    rule,
    run,
  };
}

module.exports = { createStyleSet };

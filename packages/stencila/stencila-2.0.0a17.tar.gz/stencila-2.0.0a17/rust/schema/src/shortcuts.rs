//! Shortcut functions for conveniently creating nodes of various types

use crate::{
    Article, AudioObject, Block, CodeFragment, Cord, Emphasis, Heading, ImageObject, Inline, Link,
    List, ListItem, ListOrder, Node, Paragraph, Quote, Section, Strikeout, Strong, Subscript,
    Superscript, Table, TableCell, TableCellType, TableRow, Text, Underline, VideoObject,
};

/// Create an [`Inline::Text`] node
pub fn text<S: Into<String>>(value: S) -> Inline {
    Inline::Text(Text::new(Cord::new(value.into())))
}

/// Create an [`Inline::Audio`] node
pub fn audio<S: Into<String>>(url: S) -> Inline {
    Inline::AudioObject(AudioObject::new(url.into()))
}

/// Create an [`Inline::Image`] node
pub fn img<S: Into<String>>(url: S) -> Inline {
    Inline::ImageObject(ImageObject::new(url.into()))
}

/// Create an [`Inline::Video`] node
pub fn video<S: Into<String>>(url: S) -> Inline {
    Inline::VideoObject(VideoObject::new(url.into()))
}

/// Create an [`Inline::Emphasis`] node
pub fn em<I: Into<Vec<Inline>>>(content: I) -> Inline {
    Inline::Emphasis(Emphasis::new(content.into()))
}

/// Create an [`Inline::Quote`] node
pub fn q<I: Into<Vec<Inline>>>(content: I) -> Inline {
    Inline::Quote(Quote::new(content.into()))
}

/// Create an [`Inline::Strong`] node
pub fn strong<I: Into<Vec<Inline>>>(content: I) -> Inline {
    Inline::Strong(Strong::new(content.into()))
}

/// Create an [`Inline::Strikeout`] node
pub fn s<I: Into<Vec<Inline>>>(content: I) -> Inline {
    Inline::Strikeout(Strikeout::new(content.into()))
}

/// Create an [`Inline::Subscript`] node
pub fn sub<I: Into<Vec<Inline>>>(content: I) -> Inline {
    Inline::Subscript(Subscript::new(content.into()))
}

/// Create an [`Inline::Superscript`] node
pub fn sup<I: Into<Vec<Inline>>>(content: I) -> Inline {
    Inline::Superscript(Superscript::new(content.into()))
}

/// Create an [`Inline::Underline`] node
pub fn u<I: Into<Vec<Inline>>>(content: I) -> Inline {
    Inline::Underline(Underline::new(content.into()))
}

/// Create an [`Inline::Link`] node
pub fn link<I: Into<Vec<Inline>>, S: Into<String>>(content: I, target: S) -> Inline {
    Inline::Link(Link::new(content.into(), target.into()))
}

/// Create an [`Inline::CodeFragment`] node
pub fn cf<S: Into<String>>(code: S) -> Inline {
    Inline::CodeFragment(CodeFragment::new(Cord::new(code.into())))
}

/// Create a [`Block::Heading`] node with `level: 1`
pub fn h1<I: Into<Vec<Inline>>>(content: I) -> Block {
    Block::Heading(Heading::new(1, content.into()))
}

/// Create a [`Block::Heading`] node with `level: 2`
pub fn h2<I: Into<Vec<Inline>>>(content: I) -> Block {
    Block::Heading(Heading::new(2, content.into()))
}

/// Create a [`Block::Heading`] node with `level: 3`
pub fn h3<I: Into<Vec<Inline>>>(content: I) -> Block {
    Block::Heading(Heading::new(3, content.into()))
}

/// Create a [`Block::Heading`] node with `level: 4`
pub fn h4<I: Into<Vec<Inline>>>(content: I) -> Block {
    Block::Heading(Heading::new(4, content.into()))
}

/// Create a [`Block::Heading`] node with `level: 5`
pub fn h5<I: Into<Vec<Inline>>>(content: I) -> Block {
    Block::Heading(Heading::new(5, content.into()))
}

/// Create a [`Block::Heading`] node with `level: 6`
pub fn h6<I: Into<Vec<Inline>>>(content: I) -> Block {
    Block::Heading(Heading::new(6, content.into()))
}

/// Create a [`Block::Paragraph`] node
pub fn p<I: Into<Vec<Inline>>>(content: I) -> Block {
    Block::Paragraph(Paragraph::new(content.into()))
}

/// Create a [`Block::List`] node with ascending order
pub fn ol<I: Into<Vec<ListItem>>>(items: I) -> Block {
    Block::List(List::new(items.into(), ListOrder::Ascending))
}

/// Create a [`Block::List`] node with no ordering
pub fn ul<I: Into<Vec<ListItem>>>(items: I) -> Block {
    Block::List(List::new(items.into(), ListOrder::Unordered))
}

/// Create a [`ListItem`] node
pub fn li<I: Into<Vec<Inline>>>(content: I) -> ListItem {
    ListItem {
        content: vec![p(content)],
        ..Default::default()
    }
}

/// Create a [`Block::Table`] node
pub fn table<I: Into<Vec<TableRow>>>(rows: I) -> Block {
    Block::Table(Table {
        rows: rows.into(),
        ..Default::default()
    })
}

/// Create a [`TableRow`] node
pub fn tr<I: Into<Vec<TableCell>>>(cells: I) -> TableRow {
    TableRow {
        cells: cells.into(),
        ..Default::default()
    }
}

/// Create a [`TableCell`] node with [`TableCellType::Header`]
pub fn th<I: Into<Vec<Inline>>>(content: I) -> TableCell {
    TableCell {
        cell_type: Some(TableCellType::Header),
        content: vec![p(content)],
        ..Default::default()
    }
}

/// Create a [`TableCell`] node with [`TableCellType::Data`]
pub fn td<I: Into<Vec<Inline>>>(content: I) -> TableCell {
    TableCell {
        content: vec![p(content)],
        ..Default::default()
    }
}

/// Create a [`Block::Section`] node
pub fn section<I: Into<Vec<Block>>>(content: I) -> Block {
    Block::Section(Section::new(content.into()))
}

/// Create a [`Node::Article`] node
pub fn article<I: Into<Vec<Block>>>(content: I) -> Node {
    Node::Article(Article::new(content.into()))
}

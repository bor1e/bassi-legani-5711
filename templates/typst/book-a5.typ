// =============================================================================
// BASI LEGANI - A5 BROSCHÜRE (Einspaltig)
// =============================================================================

// --- Farben & Maße ---
#let chaptercolor = rgb("#8B4513")
#let highlightcolor = rgb("#FFF3B0")
#let commentarybg = rgb("#FAFAFA")
#let summarybg = rgb("#F0F0F0")

// --- Schriften ---
#set text(font: ("Linux Libertine", "Times New Roman", "serif"), size: 11pt, lang: "de")
#let hebrew-font = ("SBL Hebrew", "David CLM", "Arial", "sans-serif")
#set par(justify: true, leading: 0.75em) // Etwas mehr Zeilenabstand für A5 Lesbarkeit

// --- PAGE SETUP (A5) ---
#set page(
  paper: "a5",
  margin: (x: 1.2cm, y: 1.5cm),
  header: context {
    if counter(page).get().first() > 3 {
      align(center, text(0.85em, style: "italic", "Bassi Legani 5711"))
      line(length: 100%, stroke: 0.5pt)
    }
  },
  footer: context {
    if counter(page).get().first() > 3 {
      align(center, counter(page).display())
    }
  }
)

// --- Hilfsfunktionen ---
#let hebhl(content) = { box(fill: none, inset: 0pt, outset: (y: 2pt), radius: 2pt, { show "\"": "״"; show "'": "׳"; text(font: hebrew-font, lang: "he", dir: rtl, content) }) }
#let heb(content) = { show "\"": "״"; show "'": "׳"; text(font: hebrew-font, lang: "he", dir: rtl, content) }
#let dehl(content) = { text(weight: "bold", content) }

// --- BLOCK ELEMENTE ---

#let verse(german: [], hebrew: [], source: none) = {
  block(width: 100%, breakable: false, spacing: 1.4em)[
    #align(right)[ #heb(hebrew) ]
    #v(0.2em)
    #german
    #if source != none { 
        v(0.2em, weak: true) 
        align(right, text(0.75em, style: "italic", fill: gray, source)) 
    }
  ]
}

#let commentary(content) = {
  block(fill: commentarybg, stroke: (left: 2pt + chaptercolor), inset: 10pt, width: 100%, radius: 2pt, spacing: 1.2em, text(size: 0.95em, style: "italic", content))
}

#let summary(content) = {
  v(0.5em)
  block(fill: summarybg, inset: 10pt, width: 100%, radius: 4pt, stroke: 0.5pt + chaptercolor, [ #text(0.9em, weight: "bold", fill: chaptercolor, "Zusammenfassung"); #v(0.5em); #text(size: 0.9em, content) ])
  v(1em)
}

#let infobox(content) = {
  v(0.5em)
  block(
    width: 100%,
    fill: rgb("#fafafa"),
    stroke: (
      top: 4pt + chaptercolor,
      bottom: 0.5pt + gray.lighten(50%),
      left: 0.5pt + gray.lighten(50%),
      right: 0.5pt + gray.lighten(50%)
    ),
    inset: (x: 0.8em, y: 1em),
    radius: 0pt,
    spacing: 1.2em,
    breakable: false,
    [
      #set text(font: ("Arial", "Helvetica", "sans-serif"), size: 0.9em, style: "italic", fill: black.lighten(20%))
      #set par(leading: 0.65em, justify: true)
      #content
    ]
  )
  v(0.5em)
}

#let dedication(content) = {
  v(1em)
  align(center)[
    #block(
      width: 95%, 
      stroke: (top: 0.5pt + chaptercolor, bottom: 0.5pt + chaptercolor), 
      inset: (y: 1em, x: 0.5em),
      spacing: 0.5em,
      [
        #set text(size: 0.9em, style: "italic", fill: black.lighten(20%))
        #set par(leading: 0.6em, justify: false)
        #content
      ]
    )
  ]
  v(1em)
}

#let glossary-term(term, definition) = {
  block(width: 100%, breakable: false, spacing: 1.2em)[
    #text(weight: "bold", fill: chaptercolor, term)
    #par(justify: true, leading: 0.7em, spacing: 0.3em)[ #definition ]
  ]
}

// =============================================================================
// LAYOUT TEMPLATES (DEFINITIONS)
// =============================================================================

// 1. DEFINITION: VORWORT (Intro)
#let layout_intro(title: "", content) = {
  pagebreak()
  set page(background: none)
  
  v(1em)
  heading(level: 1, outlined: false, title)
  v(1em)
  
  block[
    #set text(size: 1.1em) // Leicht größer für Intro
    #set par(leading: 0.8em)
    #content
  ]
}

// 2. DEFINITION: HAUPTTEIL (Main) - A5 Version
#let layout_main(title: "", hebrew-title: "", content) = {
  
  // Neues Kapitel auf neuer Seite beginnen
  pagebreak(weak: true)

  // Header Block
  if title != "" {
    block(breakable: false, width: 100%)[
      #place(hide(heading(level: 1, title)))
      
      #align(center)[
        #block(width: 100%, stroke: (bottom: 1pt + chaptercolor), inset: (bottom: 0.5em))[
          #text(1.4em, weight: "bold", fill: chaptercolor, title)
          #if hebrew-title != "" {
            h(0.5em)
            text(1.2em, font: hebrew-font, lang: "he", fill: chaptercolor, hebrew-title)
          }
        ]
      ]
    ]
    v(1em)
  }

  // Content
  content
}

// =============================================================================
// CONTENT FLOW STARTS HERE
// =============================================================================

// 1. COVER PAGE (Angepasst für A5)
#page(margin: 1.0cm, header: none, footer: none)[
  #align(center + horizon)[
    #rect(width: 100%, height: 100%, stroke: (thickness: 3pt, paint: chaptercolor), radius: 0pt, inset: 0.6cm)[
      #rect(width: 100%, height: 100%, stroke: (thickness: 1pt, paint: chaptercolor), radius: 0pt)[
        #place(top + right, dx: -5pt, dy: 5pt, text(1.3em, font: hebrew-font, "ב״ה"))
        #v(1fr)
        #text(3.5em, font: hebrew-font, weight: "bold", "באתי לגני")
        #v(0.2em)
        #text(2em, font: hebrew-font, "ה'תשי״א")
        #v(2em)
        #text(2.2em, style: "italic", weight: "bold", fill: chaptercolor, "Bassi LeGani 5711")
        #v(1.5em)
        #line(length: 50%, stroke: 1pt + chaptercolor)
        #v(1.5em)
        #text(1.2em, "Der Ma'amar vom 10. Schewat 5711 (1951)")
        #v(0.5em)
        #text(1.1em, style: "italic", "Freie erläuternde Übertragung")
        #v(3em)
        #text(1.2em)[ *Der Lubawitscher Rebbe* \ Rabbi Menachem M. Schneerson ]
        #v(1fr)
      ]
    ]
  ]
]

// 2. INHALTSVERZEICHNIS
#pagebreak()

#context {
  // 1. Überschrift manuell setzen
  align(center, text(1.5em, fill: chaptercolor, "Inhalt"))
  v(1.5em)

  // 2. Alle Überschriften (Headings) abrufen, die im Outline sein sollen
  let elems = query(heading.where(outlined: true))
  
  // Temporäre Speicher für die Unterkapitel
  let sub-items = ()
  let has-previous = false

  for el in elems {
    if el.level == 1 {
      // A. Wenn wir ein neues Kapitel erreichen, drucken wir erst die 
      // Unterkapitel des VORHERIGEN Kapitels (falls vorhanden)
      if sub-items.len() > 0 {
        pad(left: 1.5em, bottom: 0.6em, {
          set text(size: 0.9em, fill: black.lighten(30%))
          set par(leading: 0.5em) // Engerer Zeilenabstand für die Liste
          sub-items.join(" · ")
        })
        sub-items = () // Liste leeren für das neue Kapitel
      } else if has-previous {
        // Falls das vorherige Kapitel keine Unterkapitel hatte, etwas Abstand
        v(0.5em)
      }

      // B. Das Hauptkapitel drucken (Zeile mit Seitenzahl)
      link(el.location())[
        #block(width: 100%, spacing: 0.5em)[
          #text(weight: "bold", fill: chaptercolor, el.body)
          #box(width: 1fr, repeat[ . ]) // Die Pünktchenlinie
          #counter(page).at(el.location()).first()
        ]
      ]
      has-previous = true
      
    } else {
      // C. Es ist ein Unterkapitel (Level 2, 3 etc.)
      // Wir speichern es nur in der Liste, drucken es aber noch nicht
      sub-items.push(link(el.location(), el.body))
    }
  }

  // D. Ganz am Ende: Die Unterkapitel des allerletzten Kapitels drucken
  if sub-items.len() > 0 {
    pad(left: 1.5em, bottom: 0.6em, {
      set text(size: 0.9em, fill: black.lighten(30%))
      set par(leading: 0.5em)
      sub-items.join(" · ")
    })
  }
}

// 3. VORWORT (generated from input/5711/00-vorwort.md)
{{VORWORT}}

// 4. HAUPTTEIL GLOBAL SETUP
#pagebreak()
// Für A5 und Einspaltig: Keine Hintergrundlinie nötig, oder eine sehr feine am Rand
#set page(background: none)

// INHALT EINFÜGEN (Kein #columns Wrapper!)
{{CHAPTERS}}

// =============================================================================
// RÜCKSEITE (BACK COVER)
// =============================================================================

#pagebreak(weak: true)
#set page(
  header: none, 
  footer: none, 
  background: none, 
  margin: 1.2cm
)

#align(center + horizon)[
  #rect(width: 100%, height: 100%, stroke: (thickness: 3pt, paint: chaptercolor), radius: 0pt, inset: 0.6cm)[
    #rect(width: 100%, height: 100%, stroke: (thickness: 1pt, paint: chaptercolor), radius: 0pt)[
      
      // Flexibler Platz oben
      #v(1fr)

      // --- ZITAT / SUMMARY ---
      #block(width: 85%)[
        #text(1.5em, style: "italic", weight: "regular", fill: chaptercolor)[
          „Einen #text(weight: "bold")[Ma'amar] gilt es nicht nur zu lernen, \
          man muss ihn vielmehr #text(weight: "bold")[leben].“
        ]
      ]

      #v(2em)
      #line(length: 20%, stroke: 1pt + gray)
      #v(2em)

      // --- DEDICATION ---
      #block(width: 90%)[
        
        // Hebräisch (groß)
        #text(2em, font: hebrew-font, weight: "bold", fill: black)[לכבוד כ״ק אדמו״ר]
        
        #v(0.8em)
        
        // "Unserem Rebben"
        #text(1.5em, weight: "bold")[Unserem Rebben]
        
        #v(1.5em)
        
        // Der Widmungstext
        #text(1.2em, style: "italic")[
          Gewidmet der Erfüllung seiner Vision:
        ]
        
        #v(0.5em)
        
        #text(1.2em)[
          Die Quellen des Chassidus nach außen zu tragen, \
          keinen Juden zurückzulassen, \
          und G-tt in dieser Welt zu enthüllen.
        ]
      ]

      // Flexibler Platz unten
      #v(1fr)
      
      // Kleines Detail am Boden (optional)
      #text(0.9em, fill: gray)[Bassi LeGani 5711]
      
    ]
  ]
]
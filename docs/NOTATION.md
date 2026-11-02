# Mathematical notation and visual review

Reviewed on 2 November 2026.

The 65 integrated problems and their worked solutions use typeset derivatives, Greek parameters, fractions, subscripts, units and matrices. Physical illustrations and control diagrams have matching editable TikZ sources and PNG previews.

- All 40 PDFs compiled without missing-character, undefined-command, LaTeX-error or overfull-box warnings. Their 182 final pages were rendered and inspected; focused re-renders confirmed the corrected pages.
- All 284 distinct expressions extracted from 422 Markdown/notebook math occurrences compiled in a separate LaTeX syntax and glyph check.
- All twelve notebooks remain valid documents. Executable code cells are unchanged from the previously tested edition.
- Structural checks cover math delimiters, environments, two illustration cells per notebook and all 25 TikZ/PNG pairs.

The review corrected the torque-transform notation, an oversized filter-state matrix, concentration-unit consistency, and rounding in a retained-margin delay limit. Equipment drawings were checked against force directions, total spring stiffness, tank height datum and thermal flow assumptions.

See [the notation audit](notation-validation.json), [document hashes and page counts](document-validation.json), and [illustrated atlas](DIAGRAMS.md). LaTeX compilation does not certify every browser or Colab renderer.

## Browser check limitation

The live browser check could not be completed: the in-app browser failed to initialize, and Windows browser automation stopped because URL-policy enforcement is not supported for the available Firefox browser. No visual confirmation inside GitHub or Colab is claimed. PDF and extracted-expression checks completed independently.

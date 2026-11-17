from __future__ import annotations

import io
import json
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).parent
BIOLOGY = "https://pmc.ncbi.nlm.nih.gov/articles/PMC5076853/"
BIOR_RENDER = "https://www.biorender.com/template/tnf-pathway"


def part(icon: str, name: str, drawing: str) -> str:
    return f'<g id="{icon}-{name}" data-part="{name}">{drawing}</g>'


def svg(icon: str, groups: list[str]) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160" '
        'viewBox="0 0 160 160" stroke="#3D5963" '
        'stroke-linejoin="round" stroke-linecap="round">\n'
        + "\n".join(groups)
        + "\n</svg>\n"
    )


ICONS = [
    {
        "id": "tnf-trimer",
        "label": "TNF trimer",
        "label_zh": "TNF 三聚体",
        "description": "Three-subunit TNF ligand arranged around its receptor-facing interface.",
        "parts": ["subunit-a", "subunit-b", "subunit-c"],
        "anchors": {
            "TNFR1-binding-face": {"point": [80, 82], "normal": [0, 1], "kind": "binding"}
        },
        "scope": "Trimeric ligand schematic; subunit contours and receptor-facing surface are illustrative, not a solved TNF structure.",
        "groups": lambda i: [
            part(i, "subunit-a", """<g transform="rotate(0 80 80)">
              <path d="M80 17 C92 17 102 25 103 37 C105 49 97 58 87 63 C83 68 82 74 80 80 C77 73 75 68 71 64 C61 59 55 50 57 38 C58 26 68 17 80 17 Z" fill="#69ADB5" stroke-width="2.5"/>
              <path d="M67 34 L82 29 M66 41 L82 37 M68 48 L82 45" fill="none" stroke="#D7E8EC" stroke-width="1.8"/>
            </g>"""),
            part(i, "subunit-b", """<g transform="rotate(120 80 80)">
              <path d="M80 17 C92 17 102 25 103 37 C105 49 97 58 87 63 C83 68 82 74 80 80 C77 73 75 68 71 64 C61 59 55 50 57 38 C58 26 68 17 80 17 Z" fill="#69ADB5" stroke-width="2.5"/>
              <path d="M67 34 L82 29 M66 41 L82 37 M68 48 L82 45" fill="none" stroke="#D7E8EC" stroke-width="1.8"/>
            </g>"""),
            part(i, "subunit-c", """<g transform="rotate(240 80 80)">
              <path d="M80 17 C92 17 102 25 103 37 C105 49 97 58 87 63 C83 68 82 74 80 80 C77 73 75 68 71 64 C61 59 55 50 57 38 C58 26 68 17 80 17 Z" fill="#69ADB5" stroke-width="2.5"/>
              <path d="M67 34 L82 29 M66 41 L82 37 M68 48 L82 45" fill="none" stroke="#D7E8EC" stroke-width="1.8"/>
            </g>"""),
        ],
    },
    {
        "id": "tnfr1",
        "label": "TNFR1",
        "label_zh": "TNFR1",
        "description": "Single-pass TNFR1 with four extracellular cysteine-rich modules and a cytosolic death domain.",
        "parts": ["membrane", "transmembrane-helix", "cytosolic-linker", "crd1", "crd2", "crd3", "crd4", "death-domain"],
        "anchors": {
            "TNF-binding-tip": {"point": [80, 16], "normal": [0, -1], "kind": "binding"},
            "membrane-midplane": {"point": [80, 82], "normal": [0, -1], "kind": "membrane"},
            "TRADD-RIPK1-death-domain": {"point": [78, 142], "normal": [0, 1], "kind": "binding"},
        },
        "scope": "Canonical TNFR1 topology schematic; cysteine-rich domains and death-domain geometry are simplified.",
        "groups": lambda i: [
            part(i, "membrane", '<rect x="14" y="77" width="132" height="10" rx="5" fill="#B3D7CC" stroke-width="2.5"/>'),
            part(i, "transmembrane-helix", '<path d="M77 60 C74 66 75 72 77 78 L77 96 C77 101 83 101 83 96 L83 78 C85 72 86 66 83 60 Z" fill="#69ADB5" stroke-width="2.5"/>'),
            part(i, "cytosolic-linker", '<path d="M80 96 C77 101 83 106 80 113" fill="none" stroke="#3D5963" stroke-width="9"/><path d="M80 96 C77 101 83 106 80 113" fill="none" stroke="#69ADB5" stroke-width="5"/>'),
            part(i, "crd1", '<path transform="translate(0 2)" d="M67 25 C64 20 68 16 74 17 C79 13 83 18 88 16 C95 16 97 22 92 27 C89 31 83 33 77 31 C72 31 69 29 67 25 Z" fill="#69ADB5" stroke-width="2.5"/>'),
            part(i, "crd2", '<path transform="translate(0 2)" d="M68 38 C64 34 68 29 74 30 C79 26 84 31 89 29 C95 30 97 35 92 40 C88 44 82 45 77 43 C72 44 69 41 68 38 Z" fill="#69ADB5" stroke-width="2.5"/>'),
            part(i, "crd3", '<path transform="translate(0 2)" d="M68 51 C64 47 68 42 74 43 C79 39 84 44 89 42 C95 43 97 48 92 53 C88 57 82 58 77 56 C72 57 69 54 68 51 Z" fill="#69ADB5" stroke-width="2.5"/>'),
            part(i, "crd4", '<path transform="translate(0 2)" d="M68 64 C64 60 68 55 74 56 C79 52 84 57 89 55 C95 56 97 61 92 66 C88 70 82 71 77 69 C72 70 69 67 68 64 Z" fill="#69ADB5" stroke-width="2.5"/>'),
            part(i, "death-domain", '<path d="M63 119 C65 110 73 106 80 109 C88 105 97 112 97 121 C99 130 92 137 84 138 C76 146 65 141 63 133 C60 128 60 123 63 119 Z" fill="#69ADB5" stroke-width="2.5"/>'),
        ],
    },
    {
        "id": "tradd",
        "label": "TRADD",
        "label_zh": "TRADD",
        "description": "TRADD adaptor with an N-terminal TRAF-interacting region linked to a C-terminal death-domain bundle.",
        "parts": ["traf-binding-domain", "flexible-linker", "death-domain"],
        "anchors": {
            "TRAF2-binding": {"point": [16, 78], "normal": [-1, 0], "kind": "binding"},
            "TNFR1-death-domain": {"point": [119, 50], "normal": [0, -1], "kind": "binding"},
            "RIPK1-death-domain": {"point": [142, 80], "normal": [1, 0], "kind": "binding"},
        },
        "scope": "Domain-order schematic of TRADD; the two interaction regions are not an atomic structure.",
        "groups": lambda i: [
            part(i, "traf-binding-domain", '<path d="M20 58 C26 51 38 49 47 54 L60 62 L56 71 L61 81 L49 90 C40 97 28 93 23 86 C17 80 16 67 20 58 Z" fill="#69ADB5" stroke-width="2.5"/><path d="M28 61 L44 57 M25 69 L47 65 M28 78 L49 73" fill="none" stroke="#D7E8EC" stroke-width="1.8"/>'),
            part(i, "flexible-linker", '<path d="M59 71 C68 64 75 64 82 70 C88 75 91 82 99 82" fill="none" stroke="#69ADB5" stroke-width="8"/><path d="M59 71 C68 64 75 64 82 70 C88 75 91 82 99 82" fill="none" stroke="#3D5963" stroke-width="2.5"/>'),
            part(i, "death-domain", '<path d="M99 57 C107 49 119 49 126 55 C138 56 145 67 141 77 C145 87 137 98 126 98 C117 105 103 100 99 92 C91 84 92 66 99 57 Z" fill="#D7E8EC" stroke-width="2.5"/><path d="M105 61 L111 76 M117 57 L123 74 M131 62 L135 77" fill="none" stroke="#69ADB5" stroke-width="3.2"/>'),
        ],
    },
    {
        "id": "ripk1",
        "label": "RIPK1",
        "label_zh": "RIPK1",
        "description": "RIPK1 domain map with N-terminal kinase, ubiquitin-modified intermediate region, and C-terminal death domain.",
        "parts": ["kinase-domain", "intermediate-region", "ubiquitin-chain", "death-domain"],
        "anchors": {
            "kinase-active-site": {"point": [44, 47], "normal": [0, -1], "kind": "binding"},
            "ubiquitin-scaffold": {"point": [96, 34], "normal": [0, -1], "kind": "binding"},
            "death-domain-partner": {"point": [143, 81], "normal": [1, 0], "kind": "binding"},
        },
        "scope": "RIPK1 architecture schematic. The attached ubiquitin chain is a TNFR1-signaling context cue, not a constitutive RIPK1 state.",
        "groups": lambda i: [
            part(i, "kinase-domain", '<path d="M20 67 C19 58 26 50 36 49 C45 45 55 49 59 57 C66 61 68 70 63 77 C60 86 50 91 41 88 C32 93 22 87 21 79 C17 76 17 71 20 67 Z" fill="#69ADB5" stroke-width="2.5"/><path d="M34 57 L44 54 M31 64 L47 60 M32 72 L48 68 M39 81 L52 76" fill="none" stroke="#D7E8EC" stroke-width="1.8"/>'),
            part(i, "intermediate-region", '<path d="M62 77 C72 82 78 82 87 79 C96 76 103 75 112 76" fill="none" stroke="#3D5963" stroke-width="9"/><path d="M62 77 C72 82 78 82 87 79 C96 76 103 75 112 76" fill="none" stroke="#69ADB5" stroke-width="5"/>'),
            part(i, "ubiquitin-chain", '<path d="M84 78 C82 67 80 59 79 52 M94 77 C96 65 97 57 97 49 M104 76 C110 66 114 60 119 55" fill="none" stroke="#E4BE78" stroke-width="3"/><path d="M73 41 C77 35 84 36 87 42 C90 47 87 53 81 54 C75 56 70 51 70 46 C70 44 71 42 73 41 Z M91 39 C95 33 102 34 105 40 C108 45 105 51 99 52 C93 54 88 49 88 44 C88 42 89 40 91 39 Z M113 45 C117 39 124 40 127 46 C130 51 127 57 121 58 C115 60 110 55 110 50 C110 48 111 46 113 45 Z" fill="#E4BE78" stroke-width="2"/>'),
            part(i, "death-domain", '<path d="M107 65 C115 58 126 59 132 65 C140 67 145 75 142 83 C145 92 138 100 129 100 C121 107 111 102 108 95 C102 88 102 72 107 65 Z" fill="#D7E8EC" stroke-width="2.5"/><path d="M111 69 L116 82 M124 66 L129 80 M136 70 L138 82" fill="none" stroke="#69ADB5" stroke-width="3.2"/>'),
        ],
    },
    {
        "id": "traf2",
        "label": "TRAF2",
        "label_zh": "TRAF2",
        "description": "TRAF2 trimer schematic with N-terminal RING region, coiled-coil stalk, and C-terminal TRAF domains.",
        "parts": ["ring-finger", "coiled-coil", "traf-domain"],
        "anchors": {
            "RING-cIAP-interface": {"point": [66, 14], "normal": [0, -1], "kind": "binding"},
            "TRADD-interface": {"point": [28, 110], "normal": [-1, 0], "kind": "binding"},
        },
        "scope": "TRAF2 is shown as a three-chain adaptor assembly with domain order; subunit interfaces are illustrative.",
        "groups": lambda i: [
            part(i, "ring-finger", '<g transform="translate(0 4)"><path d="M47 26 C45 18 52 13 60 16 C66 10 74 14 75 22 C77 30 70 36 62 34 C54 39 47 34 47 26 Z M85 22 C86 14 94 10 101 15 C109 12 115 19 112 27 C111 35 102 38 96 33 C88 36 83 30 85 22 Z M65 31 C67 24 74 22 80 27 C87 23 94 28 94 35 C94 43 85 46 79 41 C72 45 64 40 65 31 Z" fill="#E4BE78" stroke-width="2.5"/><path d="M58 19 L64 27 L60 32 M99 17 L94 26 L101 31 M78 28 L84 35 L79 41" fill="none" stroke="#3D5963" stroke-width="1.8"/></g>'),
            part(i, "coiled-coil", '<path d="M59 36 C63 47 69 56 76 67 C81 75 81 84 79 94 M80 37 C84 48 89 57 84 68 C81 77 86 84 84 95 M101 36 C96 48 92 57 89 68 C86 77 90 85 89 95" fill="none" stroke="#69ADB5" stroke-width="6"/><path d="M59 36 C63 47 69 56 76 67 C81 75 81 84 79 94 M80 37 C84 48 89 57 84 68 C81 77 86 84 84 95 M101 36 C96 48 92 57 89 68 C86 77 90 85 89 95" fill="none" stroke="#3D5963" stroke-width="2.5"/>'),
            part(i, "traf-domain", '<path d="M29 108 C30 98 39 92 49 94 C58 89 68 95 69 105 C71 114 64 121 55 123 C49 131 38 129 34 123 C29 120 27 114 29 108 Z M61 112 C62 102 71 96 81 98 C90 93 100 99 101 109 C103 118 96 125 87 127 C81 135 70 133 66 127 C61 124 59 118 61 112 Z M93 108 C94 98 103 92 113 94 C122 89 132 95 133 105 C135 114 128 121 119 123 C113 131 102 129 98 123 C93 120 91 114 93 108 Z" fill="#69ADB5" stroke-width="2.5"/><path d="M40 103 L55 99 M40 111 L57 107 M72 107 L88 103 M72 115 L89 111 M104 103 L119 99 M104 111 L121 107" fill="none" stroke="#D7E8EC" stroke-width="1.8"/>'),
        ],
    },
    {
        "id": "tak1",
        "label": "TAK1",
        "label_zh": "TAK1",
        "description": "MAP3K7 schematic with a bilobal kinase domain, activation segment, and regulatory C-terminal region.",
        "parts": ["kinase-n-lobe", "kinase-c-lobe", "activation-loop", "regulatory-region"],
        "anchors": {
            "TAB-regulatory-association": {"point": [146, 103], "normal": [1, 0], "kind": "binding"},
            "IKK-phosphorylation": {"point": [76, 96], "normal": [0, 1], "kind": "binding"},
        },
        "scope": "TAK1/MAP3K7 domain schematic; activation-loop and regulatory-region geometry are illustrative.",
        "groups": lambda i: [
            part(i, "kinase-n-lobe", '<path d="M21 55 C19 42 28 31 40 30 C51 24 65 28 71 38 C78 46 75 58 67 64 C59 72 43 71 33 67 C26 65 22 61 21 55 Z" fill="#69ADB5" stroke-width="2.5"/><path d="M34 40 L48 36 M31 48 L53 44 M35 56 L56 52" fill="none" stroke="#D7E8EC" stroke-width="1.8"/>'),
            part(i, "kinase-c-lobe", '<path d="M63 66 C75 58 93 58 105 65 C118 71 125 83 123 97 C121 109 109 115 97 113 C83 120 68 113 63 103 C57 94 55 76 63 66 Z" fill="#69ADB5" stroke-width="2.5"/><path d="M77 78 L94 72 M74 87 L99 80 M78 98 L101 92" fill="none" stroke="#D7E8EC" stroke-width="1.8"/>'),
            part(i, "activation-loop", '<path d="M59 60 C67 67 72 73 70 82 C68 90 75 93 83 91 C90 89 94 84 99 82" fill="none" stroke="#E4BE78" stroke-width="5"/><circle cx="76" cy="91" r="4.5" fill="#E4BE78" stroke-width="2"/>'),
            part(i, "regulatory-region", '<path d="M108 100 C116 94 122 96 128 102 C132 107 136 106 141 103" fill="none" stroke="#3D5963" stroke-width="10"/><path d="M108 100 C116 94 122 96 128 102 C132 107 136 106 141 103" fill="none" stroke="#D7E8EC" stroke-width="5"/>'),
        ],
    },
    {
        "id": "ikk-complex",
        "label": "IKK complex",
        "label_zh": "IKK 复合体",
        "description": "Canonical IKK complex with separate IKKα and IKKβ kinase subunits and a NEMO scaffold.",
        "parts": ["ikk-alpha", "ikk-beta", "nemo-scaffold", "nemo-zinc-finger"],
        "anchors": {
            "TAK1-activation": {"point": [38, 27], "normal": [0, -1], "kind": "binding"},
            "ubiquitin-chain-binding": {"point": [143, 109], "normal": [1, 0], "kind": "binding"},
            "IkB-substrate": {"point": [76, 71], "normal": [1, 0], "kind": "binding"},
        },
        "scope": "Illustrative IKKα/IKKβ kinase pair on a NEMO scaffold; the arrangement communicates components, not exact stoichiometry or resolved geometry.",
        "groups": lambda i: [
            part(i, "nemo-scaffold", '<path d="M27 108 C45 101 61 104 78 108 C95 113 111 113 132 105 L138 117 C118 127 97 128 77 121 C60 116 45 115 30 121 Z" fill="#B3D7CC" stroke-width="2.5"/><path d="M32 113 C49 109 62 113 78 117 C95 121 111 119 130 112" fill="none" stroke="#69ADB5" stroke-width="4"/><path d="M57 88 L59 108 M121 90 L121 107" fill="none" stroke="#69ADB5" stroke-width="5"/>'),
            part(i, "ikk-alpha", '<path d="M38 27 C48 25 57 31 60 41 C62 47 60 52 56 57 C66 56 74 62 76 71 C78 81 71 90 61 93 C52 97 42 93 38 86 C29 87 22 81 21 73 C18 64 23 55 31 51 C26 41 29 31 38 27 Z" fill="#69ADB5" stroke-width="2.5"/><path d="M44 39 L54 42 M39 70 L54 76" fill="none" stroke="#D7E8EC" stroke-width="2"/>'),
            part(i, "ikk-beta", '<path d="M103 31 C114 28 124 34 127 44 C130 50 128 55 124 60 C134 59 142 65 144 74 C146 84 139 93 129 96 C120 100 110 96 106 89 C97 90 90 84 89 76 C86 67 91 58 99 54 C94 44 97 35 103 31 Z" fill="#69ADB5" stroke-width="2.5"/><path d="M109 43 L119 46 M104 74 L119 80" fill="none" stroke="#D7E8EC" stroke-width="2"/>'),
            part(i, "nemo-zinc-finger", '<path d="M131 99 C139 95 145 100 144 107 C145 114 139 119 132 117 C126 114 126 104 131 99 Z" fill="#E4BE78" stroke-width="2.5"/>'),
        ],
    },
    {
        "id": "ikba",
        "label": "IκBα",
        "label_zh": "IκBα",
        "description": "IκBα with a curved ankyrin-repeat core, N-terminal phosphodegron, and flexible PEST tail.",
        "parts": ["n-terminal-phosphodegron", "ankyrin-repeat-domain", "pest-tail"],
        "anchors": {
            "NF-kB-binding-face": {"point": [38, 83], "normal": [-1, 0], "kind": "binding"},
            "phosphodegron": {"point": [16, 22], "normal": [-1, 0], "kind": "binding"},
        },
        "scope": "IκBα domain schematic; ankyrin-repeat curvature and degron positions are illustrative, not residue-scale.",
        "groups": lambda i: [
            part(i, "n-terminal-phosphodegron", '<path d="M42 40 C34 33 27 27 20 20" fill="none" stroke="#69ADB5" stroke-width="5"/><circle cx="21" cy="21" r="5" fill="#E4BE78" stroke-width="2"/><circle cx="30" cy="30" r="4.5" fill="#E4BE78" stroke-width="2"/>'),
            part(i, "ankyrin-repeat-domain", '<path d="M49 34 C58 29 69 31 75 38 C80 44 77 50 69 52 C60 54 50 51 46 46 C44 42 45 37 49 34 Z M45 49 C54 44 66 46 72 53 C77 59 74 65 66 67 C57 69 47 66 43 61 C41 57 42 52 45 49 Z M42 64 C51 59 63 61 69 68 C74 74 71 80 63 82 C54 84 44 81 40 76 C38 72 39 67 42 64 Z M40 79 C49 74 61 76 67 83 C72 89 69 95 61 97 C52 99 42 96 38 91 C36 87 37 82 40 79 Z M40 94 C49 89 61 91 67 98 C72 104 69 110 61 112 C52 114 42 111 38 106 C36 102 37 97 40 94 Z M44 109 C53 104 65 106 71 113 C76 119 73 125 65 127 C56 129 46 126 42 121 C40 117 41 112 44 109 Z" fill="#D7E8EC" stroke-width="2.5"/><path d="M51 39 C57 35 65 36 69 41 M47 54 C54 50 63 51 67 56 M44 69 C51 65 60 66 64 71 M42 84 C49 80 58 81 62 86 M42 99 C49 95 58 96 62 101 M46 114 C53 110 62 111 66 116" fill="none" stroke="#69ADB5" stroke-width="1.8"/>'),
            part(i, "pest-tail", '<path d="M66 125 C75 132 82 136 91 134 C100 132 103 139 110 139 C117 139 122 134 128 137 C134 140 139 144 145 141" fill="none" stroke="#B2A6CD" stroke-width="5"/>'),
        ],
    },
    {
        "id": "rela",
        "label": "RELA / p65",
        "label_zh": "RELA / p65",
        "description": "RELA p65 with a two-lobe Rel homology domain, DNA-contact loops, and a flexible C-terminal transactivation region.",
        "parts": ["dna-binding-lobe", "dimerization-lobe", "dna-contact-loops", "transactivation-region"],
        "anchors": {
            "p50-dimer-interface": {"point": [110, 85], "normal": [1, 0], "kind": "binding"},
            "DNA-binding-surface": {"point": [19, 58], "normal": [-1, 0], "kind": "binding"},
            "transactivation-region": {"point": [145, 139], "normal": [1, 0], "kind": "binding"},
        },
        "scope": "RELA/p65 schematic; the Rel homology domain is simplified and the disordered transactivation region is shown as a flexible tail.",
        "groups": lambda i: [
            part(i, "dna-binding-lobe", '<path d="M25 40 C22 29 32 20 46 19 C59 18 69 27 71 39 C73 50 66 61 56 66 C44 71 31 63 26 53 C22 49 22 44 25 40 Z" fill="#69ADB5" stroke-width="2.5"/><path d="M35 31 L50 26 M33 40 L53 35 M37 49 L56 44 M44 58 L58 53" fill="none" stroke="#D7E8EC" stroke-width="1.8"/>'),
            part(i, "dimerization-lobe", '<g transform="translate(-6 -4)"><path d="M63 62 C76 52 95 54 107 63 C118 72 120 89 111 100 C103 111 85 114 72 106 C60 98 57 75 63 62 Z" fill="#69ADB5" stroke-width="2.5"/><path d="M73 70 L91 65 M69 80 L98 74 M71 92 L98 87 M82 103 L103 98" fill="none" stroke="#D7E8EC" stroke-width="1.8"/></g>'),
            part(i, "dna-contact-loops", '<path d="M27 48 C20 51 18 58 23 63 C27 67 33 66 37 63 M30 57 C24 61 23 68 28 72 C32 75 37 72 41 69" fill="none" stroke="#E4BE78" stroke-width="4"/>'),
            part(i, "transactivation-region", '<path d="M106 101 C114 108 119 116 115 123 C112 129 117 134 124 132 C131 130 135 134 140 139" fill="none" stroke="#3D5963" stroke-width="10"/><path d="M106 101 C114 108 119 116 115 123 C112 129 117 134 124 132 C131 130 135 134 140 139" fill="none" stroke="#D7E8EC" stroke-width="5"/>'),
        ],
    },
    {
        "id": "nfkb1-p50",
        "label": "NFKB1 / p50",
        "label_zh": "NFKB1 / p50",
        "description": "Mature NFKB1 p50 with paired Rel homology DNA-binding and dimerization lobes.",
        "parts": ["dna-binding-lobe", "dimerization-lobe", "dna-contact-loops"],
        "anchors": {
            "p65-dimer-interface": {"point": [112, 87], "normal": [1, 0], "kind": "binding"},
            "DNA-binding-surface": {"point": [19, 59], "normal": [-1, 0], "kind": "binding"},
        },
        "scope": "Mature NFKB1 p50 schematic; the Rel homology domain is simplified. The p105 precursor and its processing are not depicted.",
        "groups": lambda i: [
            part(i, "dna-binding-lobe", '<path d="M26 42 C23 31 33 22 47 21 C60 20 70 29 72 41 C74 52 67 63 57 68 C45 73 32 65 27 55 C23 51 23 46 26 42 Z" fill="#D7E8EC" stroke-width="2.5"/><path d="M36 33 L51 28 M34 42 L54 37 M38 51 L57 46 M45 60 L59 55" fill="none" stroke="#69ADB5" stroke-width="1.8"/>'),
            part(i, "dimerization-lobe", '<g transform="translate(-6 -4)"><path d="M65 64 C78 54 97 56 109 65 C120 74 122 91 113 102 C105 113 87 116 74 108 C62 100 59 77 65 64 Z" fill="#D7E8EC" stroke-width="2.5"/><path d="M75 72 L93 67 M71 82 L100 76 M73 94 L100 89 M84 105 L105 100" fill="none" stroke="#69ADB5" stroke-width="1.8"/></g>'),
            part(i, "dna-contact-loops", '<path d="M28 50 C21 53 19 60 24 65 C28 69 34 68 38 65 M31 59 C25 63 24 70 29 74 C33 77 38 74 42 71" fill="none" stroke="#E4BE78" stroke-width="4"/>'),
        ],
    },
    {
        "id": "proteasome-26s",
        "label": "26S proteasome",
        "label_zh": "26S 蛋白酶体",
        "description": "Doubly capped 26S proteasome schematic with 19S regulators, a 20S core barrel, and a central substrate channel.",
        "parts": ["19s-top", "20s-alpha-rings", "20s-beta-rings", "19s-bottom", "substrate-channel"],
        "anchors": {
            "ubiquitinated-substrate-entry": {"point": [80, 17], "normal": [0, -1], "kind": "binding"},
            "peptide-release": {"point": [80, 143], "normal": [0, 1], "kind": "binding"},
        },
        "scope": "Doubly capped 26S proteasome schematic; subunit stoichiometry and molecular geometry are simplified.",
        "groups": lambda i: [
            part(i, "19s-top", '<path d="M42 17 C49 12 58 13 65 17 L95 17 C102 13 111 12 118 17 C124 23 122 31 116 36 L44 36 C38 31 36 23 42 17 Z" fill="#B3D7CC" stroke-width="2.5"/><path d="M50 24 C61 20 70 23 80 23 C90 23 99 20 110 24" fill="none" stroke="#69ADB5" stroke-width="3"/>'),
            part(i, "20s-alpha-rings", '<path d="M31 39 C43 35 57 37 68 40 L92 40 C103 37 117 35 129 39 L129 59 C117 63 104 61 92 58 L68 58 C56 61 43 63 31 59 Z" fill="#69ADB5" stroke-width="2.5"/><path d="M31 61 C43 57 57 59 68 62 L92 62 C103 59 117 57 129 61 L129 81 C117 85 104 83 92 80 L68 80 C56 83 43 85 31 81 Z" fill="#D7E8EC" stroke-width="2.5"/>'),
            part(i, "20s-beta-rings", '<path d="M31 83 C43 79 57 81 68 84 L92 84 C103 81 117 79 129 83 L129 103 C117 107 104 105 92 102 L68 102 C56 105 43 107 31 103 Z" fill="#69ADB5" stroke-width="2.5"/><path d="M31 105 C43 101 57 103 68 106 L92 106 C103 103 117 101 129 105 L129 121 C117 125 104 123 92 120 L68 120 C56 123 43 125 31 121 Z" fill="#D7E8EC" stroke-width="2.5"/>'),
            part(i, "19s-bottom", '<path d="M44 124 L116 124 C122 129 124 137 118 142 C111 145 102 145 95 143 L65 143 C58 145 49 145 42 142 C36 137 38 129 44 124 Z" fill="#B3D7CC" stroke-width="2.5"/><path d="M50 135 C61 131 70 134 80 134 C90 134 99 131 110 135" fill="none" stroke="#69ADB5" stroke-width="3"/>'),
            part(i, "substrate-channel", '<path d="M77 40 L83 40 L83 120 L77 120 Z" fill="#FFFFFF" stroke-width="1.8"/><path d="M70 58 C75 61 85 61 90 58 M70 80 C75 83 85 83 90 80 M70 102 C75 105 85 105 90 102" fill="none" stroke="#3D5963" stroke-width="1.6"/><path d="M80 20 L80 41" fill="none" stroke="#E4BE78" stroke-width="3"/>'),
        ],
    },
]


def build() -> None:
    manifest = []
    for icon in ICONS:
        groups = icon["groups"](icon["id"])
        (OUT / f'{icon["id"]}.svg').write_text(svg(icon["id"], groups))
        entry = {
            "id": icon["id"],
            "label": icon["label"],
            "label_zh": icon["label_zh"],
            "file": f'nfkb/{icon["id"]}.svg',
            "category": "signaling",
            "description": icon["description"],
            "parts": icon["parts"],
            "anchors": icon["anchors"],
            "scope": icon["scope"],
            "provenance": {
                "mode": "original-vector",
                "visual_references": [BIOR_RENDER],
                "scientific_references": [BIOLOGY],
                "license": "MIT",
            },
        }
        manifest.append(entry)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
    cols, cell_w, cell_h = 4, 240, 242
    rows = (len(ICONS) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "#FFFFFF")
    draw = ImageDraw.Draw(sheet)
    for index, icon in enumerate(ICONS):
        x = (index % cols) * cell_w
        y = (index // cols) * cell_h
        draw.rounded_rectangle((x + 10, y + 8, x + cell_w - 10, y + cell_h - 8), radius=12, fill="#FBFDFC", outline="#DCE8E6", width=2)
        png = cairosvg.svg2png(url=str(OUT / f'{icon["id"]}.svg'), output_width=178, output_height=178)
        art = Image.open(io.BytesIO(png)).convert("RGBA")
        sheet.paste(art, (x + (cell_w - 178) // 2, y + 13), art)
        label = icon["label"]
        bounds = draw.textbbox((0, 0), label, font=font)
        draw.text((x + (cell_w - (bounds[2] - bounds[0])) / 2, y + 195), label, font=font, fill="#20343B")
    sheet.save(OUT / "contact-sheet.png", optimize=True)


if __name__ == "__main__":
    build()

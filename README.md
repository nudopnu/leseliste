# Leseliste 📖

```bash
uv init
uv run leseliste "SAFE-Hair: Scalp-Anchored Fields for Exportable Single-View Hair Reconstruction"
```




<details><summary>JSON Ausgabe</summary>

```json
{
    "topic": "SAFE-Hair: Scalp-Anchored Fields for Exportable Single-View Hair Reconstruction",
    "introduction": "SAFE-Hair ist ein aktuelles Forschungspaper (NeurIPS 2026), das aus einem einzelnen Porträtfoto eine vollständige 3D-Haarrekonstruktion auf Strand-Ebene erzeugt. Das Besondere: Die rekonstruierten Haare sind an einer kanonischen Kopfhaut-UV-Parametrisierung verankert, editierbar und direkt in Produktions-Pipelines (z.B. Blender, Unreal Engine) exportierbar. Um dieses Paper wirklich zu verstehen, brauchst du Wissen aus mehreren Bereichen: Vision Transformers und selbstüberwachte Bildfeatures (DINOv2), 3D-Kopfmodelle (FLAME), generative Modelle (Diffusion/Flow Matching/Rectified Flow) und die Domäne der computergrafischen Haarmodellierung. Dieser Lernpfad führt dich systematisch durch all diese Bausteine.",
    "learning_objectives": [
        "Verstehen, wie selbstüberwachte Vision-Features (DINOv2) semantisch reichhaltige Bildrepräsentationen liefern",
        "3D Morphable Models (speziell FLAME) und UV-Parametrisierung einer Kopfoberfläche verstehen",
        "Flow Matching und Rectified Flow als generative Modellierungstechnik erklären können",
        "Die vollständige SAFE-Hair-Pipeline nachvollziehen: von Bild-Features über Scalp-UV-Projektion, Rectified Flow auf Scalp Fields bis zur Strand-Dekodierung",
        "Strand-basierte Haarrepräsentationen verstehen und mit Produktionstools (Alembic-Export) arbeiten können",
        "Evaluationsmetriken für 3D-Haarrekonstruktion (Chamfer Distance, F-Score, Root Validity) interpretieren können"
    ],
    "assumed_knowledge": [
        "Grundlegendes Verständnis von Deep Learning (Backpropagation, Loss-Funktionen, Training)",
        "Python-Programmierkenntnisse",
        "Basiswissen lineare Algebra (Matrizen, Transformationen)",
        "Grundkenntnisse in PyTorch oder einem ähnlichen Framework",
        "Grundverständnis von Bildern als Datenstruktur (Pixel, Kanäle, Auflösung)"
    ],
    "learning_path": [
        {
            "phase": 1,
            "title": "Einstieg: Vision Transformers und selbstüberwachte Features",
            "description": "Bevor du SAFE-Hair verstehen kannst, musst du wissen, wie das System aus einem Bild semantisch reichhaltige Features extrahiert. SAFE-Hair nutzt DINOv2 – ein selbstüberwachtes Vision-Transformer-Modell von Meta. In dieser Phase lernst du, was Vision Transformers sind und wie DINOv2 ohne Labels lernt, nützliche Bildfeatures zu erzeugen.",
            "resources": [
                {
                    "type": "blog",
                    "title": "An Image is Worth 16x16 Words: A Visual Guide to Vision Transformers (ViT)",
                    "authors": [
                        "Jay Alammar"
                    ],
                    "publisher": null,
                    "year": 2024,
                    "url": "https://jalammar.github.io/illustrated-transformer/",
                    "priority": "essential",
                    "estimated_hours": 2,
                    "reason": "Jay Alammar ist bekannt für hervorragende visuelle Erklärungen komplexer ML-Konzepte. Sein Illustrated Transformer Post erklärt die Grundarchitektur, auf der ViT und damit auch DINOv2 aufbauen. Du brauchst dieses Fundament, um zu verstehen, wie Patch-Embeddings und Self-Attention funktionieren.",
                    "recommended_sections": [
                        {
                            "name": "Self-Attention und Multi-Head Attention",
                            "focus": "Verstehe, wie Tokens miteinander interagieren und warum Attention die Grundlage für das Lernen räumlicher Beziehungen ist",
                            "verified": false
                        },
                        {
                            "name": "Positional Encoding",
                            "focus": "Wichtig für das Verständnis, wie räumliche Information in Transformern erhalten bleibt",
                            "verified": false
                        }
                    ],
                    "takeaways": [
                        "Transformer-Architektur: Encoder-Struktur mit Self-Attention",
                        "Wie ein Bild in Patches aufgeteilt und als Token-Sequenz behandelt wird",
                        "Warum Positional Encodings nötig sind, wenn man Patches statt Pixel verarbeitet"
                    ],
                    "practical_exercises": [
                        "Visualisiere die Attention-Maps eines vortrainierten ViT-Modells auf eigenen Bildern mit dem timm-Package in PyTorch",
                        "Experimentiere mit verschiedenen Patch-Größen und beobachte den Einfluss auf die Feature-Auflösung"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Warum teilt ein Vision Transformer ein Bild in Patches auf, anstatt einzelne Pixel als Tokens zu verwenden? Welche Konsequenz hat die Patch-Größe?",
                            "answer": "Einzelne Pixel als Tokens würden zu einer extrem langen Sequenz führen (z.B. 224×224 = 50.176 Tokens), was wegen der quadratischen Komplexität der Self-Attention nicht handhabbar wäre. Durch die Aufteilung in z.B. 16×16-Patches reduziert sich die Sequenzlänge auf 196 Tokens (bei 224×224 Bildern). Die Patch-Größe bestimmt den Trade-off zwischen räumlicher Auflösung der Features und Rechenaufwand: Kleinere Patches liefern feinere räumliche Details, kosten aber quadratisch mehr Rechenzeit in der Attention."
                        },
                        {
                            "question": "Was ist der fundamentale Unterschied zwischen CNN-Features und ViT-Features in Bezug auf den rezeptiven Bereich (receptive field)?",
                            "answer": "CNNs bauen ihren rezeptiven Bereich hierarchisch auf – frühe Schichten sehen nur lokale Nachbarschaften, und erst tiefe Schichten aggregieren globale Information. Ein ViT hingegen hat durch Self-Attention von der ersten Schicht an einen globalen rezeptiven Bereich: Jeder Patch kann direkt mit jedem anderen Patch interagieren. Das bedeutet, dass ViT-Features schon in frühen Layern globalen Kontext einbeziehen können, was besonders für Aufgaben wie Haarrekonstruktion wertvoll ist, wo die Gesamtstruktur der Frisur den lokalen Strandverlauf beeinflusst."
                        },
                        {
                            "question": "Warum sind die Patch-Level-Features eines ViT besonders nützlich für Dense-Prediction-Aufgaben wie die Projektion auf eine Kopfhaut-UV-Map?",
                            "answer": "Jeder Patch-Token in einem ViT repräsentiert nach den Transformer-Layern nicht nur seinen lokalen Bildausschnitt, sondern hat durch Self-Attention auch globalen Kontext über das gesamte Bild integriert. Für die Projektion auf eine Scalp-UV-Map bedeutet das: Wenn SAFE-Hair die DINOv2-Features auf die Kopfhautoberfläche projiziert, trägt jeder projizierte Feature-Vektor Information über die lokale Haarstruktur UND den globalen Frisurkontext. Das hilft dem Modell, auch für nicht sichtbare Regionen (Hinterkopf) plausible Haarstrukturen zu generieren."
                        }
                    ]
                },
                {
                    "type": "blog",
                    "title": "DINOv2 — Self-Supervised Vision Features: Step-by-Step Explanation",
                    "authors": [
                        "Picsellia Team"
                    ],
                    "publisher": "Picsellia",
                    "year": 2023,
                    "url": "https://www.picsellia.com/post/dinov2-steps-by-steps-explanations-picsellia",
                    "priority": "essential",
                    "estimated_hours": 1.5,
                    "reason": "Erklärt DINOv2 Schritt für Schritt und zugänglich. Du musst verstehen, wie DINOv2 ohne gelabelte Daten lernt, semantisch reichhaltige Features zu erzeugen – das ist die Grundlage dafür, wie SAFE-Hair Bildinformation auf die Kopfhaut projiziert.",
                    "recommended_sections": [
                        {
                            "name": "Self-Distillation Mechanism",
                            "focus": "Verstehe das Teacher-Student-Setup und warum es ohne Labels funktioniert",
                            "verified": false
                        },
                        {
                            "name": "Feature Properties",
                            "focus": "Achte darauf, welche Arten von semantischer Information in den Features kodiert sind",
                            "verified": false
                        }
                    ],
                    "takeaways": [
                        "DINOv2 lernt durch Self-Distillation: Ein Student-Netzwerk lernt, die Outputs eines Teacher-Netzwerks (EMA des Students) zu matchen",
                        "Die Features sind universell einsetzbar für Klassifikation, Segmentierung, Tiefenschätzung – ohne Fine-Tuning",
                        "Patch-Level-Features enthalten dichte semantische Information, die für Downstream-Aufgaben wie UV-Projektion ideal ist"
                    ],
                    "practical_exercises": [
                        "Lade ein vortrainiertes DINOv2-Modell und extrahiere Features für verschiedene Porträtfotos. Visualisiere die PCA der Patch-Features – du wirst sehen, dass Haarregionen semantisch kohärente Cluster bilden",
                        "Vergleiche DINOv2-Features mit CLIP-Features auf denselben Bildern: Welche sind räumlich kohärenter?"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Warum nutzt SAFE-Hair DINOv2-Features statt z.B. Features eines auf ImageNet supervised trainierten ResNet?",
                            "answer": "DINOv2-Features haben mehrere entscheidende Vorteile: (1) Sie sind semantisch reichhaltiger, weil Self-Distillation das Modell zwingt, invariante Repräsentationen über verschiedene Augmentierungen zu lernen. (2) Sie generalisieren besser auf neue Domänen (wie Porträtfotos), weil sie nicht auf ImageNet-Kategorien überangepasst sind. (3) Die Patch-Level-Features sind besonders dicht und kohärent – benachbarte Patches mit ähnlicher Semantik (z.B. gleicher Haartexturregion) haben ähnliche Features. Das ist entscheidend für die Projektion auf die Scalp-UV-Map, wo räumliche Kohärenz der projizierten Features die Qualität der generierten Scalp Fields bestimmt."
                        },
                        {
                            "question": "Was bedeutet es konkret, wenn man sagt, DINOv2-Features seien 'self-supervised'? Welchen Vorteil hat das für ein System wie SAFE-Hair?",
                            "answer": "'Self-supervised' bedeutet, dass das Modell seine Trainings-Supervision aus den Daten selbst generiert, ohne menschliche Annotationen. Bei DINOv2 geschieht das durch Self-Distillation: Verschiedene augmentierte Ansichten desselben Bildes sollen ähnliche Repräsentationen erzeugen. Der Vorteil für SAFE-Hair ist dreifach: Erstens kann DINOv2 auf einer riesigen, unlabelierten Bildsammlung trainiert werden (viel mehr Daten als gelabelte Datensätze). Zweitens lernt es allgemeine visuelle Konzepte statt aufgabenspezifischer Features. Drittens sind die gelernten Features robust gegenüber Variationen in Beleuchtung, Pose und Hintergrund – genau die Variationen, die bei Porträtfotos in der Praxis auftreten."
                        },
                        {
                            "question": "Wie hängen die räumlichen Positionen der DINOv2-Patch-Features mit der späteren Projektion auf die Scalp-UV-Map zusammen?",
                            "answer": "Jeder DINOv2-Patch-Token entspricht einer bestimmten räumlichen Position im Eingabebild. SAFE-Hair passt zunächst ein FLAME-Kopfmodell an das Bild an und kennt dadurch die 3D-Geometrie des Kopfes und die Kameraprojektion. Für jeden Punkt auf der Kopfhautoberfläche kann es berechnen, in welchen Bildbereich dieser Punkt projiziert wird – und damit, welcher DINOv2-Patch-Token die relevante visuelle Information enthält. So wird eine dichte Scalp-UV-Feature-Map konstruiert, bei der jede UV-Position die visuellen Features der dort sichtbaren Haare trägt. Für Regionen, die im Bild nicht sichtbar sind (z.B. Hinterkopf), fehlen direkte Features – hier kommt dann das Rectified-Flow-Modell ins Spiel, das diese Lücken plausibel füllt."
                        }
                    ]
                }
            ],
            "milestone": "Du kannst erklären, wie ein Vision Transformer Bilder verarbeitet und warum DINOv2-Features besonders geeignet sind, um Bildinformation auf 3D-Oberflächen zu projizieren. Du kannst DINOv2-Features in PyTorch extrahieren und visualisieren."
        },
        {
            "phase": 2,
            "title": "3D-Kopfmodelle und UV-Parametrisierung",
            "description": "SAFE-Hair verankert alle Haarsträhnen an einer kanonischen Kopfhautoberfläche im UV-Raum. Dafür nutzt es ein parametrisches 3D-Kopfmodell (FLAME). Du musst verstehen, was ein 3D Morphable Model ist, wie UV-Mapping funktioniert und wie man ein Kopfmodell an ein Foto fittet.",
            "resources": [
                {
                    "type": "paper",
                    "title": "Learning a model of facial shape and expression from 4D scans (FLAME)",
                    "authors": [
                        "Tianye Li",
                        "Timo Bolkart",
                        "Michael J. Black",
                        "Hao Li",
                        "Javier Romero"
                    ],
                    "publisher": "ACM Transactions on Graphics",
                    "year": 2017,
                    "url": "https://flame.is.tue.mpg.de/",
                    "priority": "essential",
                    "estimated_hours": 2,
                    "reason": "FLAME ist DAS Standard-Kopfmodell in der aktuellen Forschung und die Basis für SAFE-Hair's Scalp-UV-Parametrisierung. Du musst nicht das gesamte Paper im Detail lesen, aber die Kernkonzepte verstehen.",
                    "recommended_sections": [
                        {
                            "name": "Abschnitt 3: Model Formulation",
                            "focus": "Verstehe die Zerlegung in Shape (Identität), Expression und Pose-Parameter. Die Formel T(β,θ,ψ) ist zentral.",
                            "verified": true
                        },
                        {
                            "name": "Abschnitt zur Scalp-Region",
                            "focus": "Achte darauf, wie die Kopfhaut als Teilmenge der Mesh-Vertices definiert ist",
                            "verified": false
                        }
                    ],
                    "takeaways": [
                        "FLAME parametrisiert einen 3D-Kopf durch Shape-Parameter (Identität), Pose-Parameter (Rotation von Hals, Kiefer, Augen) und Expression-Parameter",
                        "Das Modell ist ein Mesh mit fester Topologie – jeder Vertex hat eine feste UV-Koordinate",
                        "Die Kopfhaut ist eine definierte Teilmenge der Mesh-Oberfläche mit eigenem UV-Layout"
                    ],
                    "practical_exercises": [
                        "Klone das FLAME_PyTorch Repository (github.com/soubhiksanyal/FLAME_PyTorch), lade das Modell herunter und rendere verschiedene Identitäten und Expressionen",
                        "Visualisiere die UV-Map des FLAME-Modells und identifiziere die Scalp-Region",
                        "Fitte FLAME an ein eigenes Porträtfoto mit einem Fitting-Tool wie DECA oder MICA"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Was bedeutet es, dass FLAME eine 'feste Topologie' hat, und warum ist das für SAFE-Hair entscheidend?",
                            "answer": "Feste Topologie bedeutet, dass alle generierten Köpfe dieselbe Mesh-Struktur haben: dieselbe Anzahl Vertices, dieselben Kanten, dieselben Dreiecke – nur die Positionen der Vertices ändern sich je nach Shape- und Pose-Parametern. Für SAFE-Hair ist das entscheidend, weil es eine kanonische Scalp-UV-Domäne ermöglicht: Vertex 4237 ist bei JEDEM generierten Kopf 'der gleiche Punkt' auf der Kopfhaut. Dadurch kann SAFE-Hair Follicle-Positionen als feste UV-Koordinaten definieren, die über alle Subjekte hinweg konsistent sind. Ein Follikel an UV-Position (0.3, 0.7) ist immer an derselben semantischen Stelle auf dem Kopf, egal ob der Kopf groß oder klein, rund oder oval ist."
                        },
                        {
                            "question": "Wie unterscheidet sich die UV-Parametrisierung der Kopfhaut von einer Textur-UV-Map, und warum nutzt SAFE-Hair erstere?",
                            "answer": "Eine Textur-UV-Map ordnet jedem Punkt der 3D-Oberfläche 2D-Koordinaten zu, um Farbinformationen (Texturen) darauf abzubilden. Die Scalp-UV-Parametrisierung in SAFE-Hair nutzt dasselbe mathematische Prinzip, aber statt Farbe werden dort Haarinformationen kodiert: Occupancy (ist hier ein Haar?), Strang-Richtungen, Längenzuweisung und Gesamtlänge. Der Vorteil gegenüber einer volumetrischen 3D-Repräsentation: Die 2D-UV-Map ist kompakter und strukturierter. Neuronale Netze können mit 2D-Feature-Maps effizienter arbeiten als mit 3D-Volumina. Zudem erzwingt die Verankerung am Scalp automatisch, dass alle Strähnen an der Kopfhaut beginnen – ein physikalisch korrektes Prior."
                        },
                        {
                            "question": "Welche Rolle spielt das FLAME-Fitting im Gesamtsystem von SAFE-Hair, und was passiert, wenn das Fitting ungenau ist?",
                            "answer": "Das FLAME-Fitting ist der erste Schritt der Pipeline: Aus dem Eingabe-Porträt wird die 3D-Kopfgeometrie und die Kamerapose geschätzt. Dies ermöglicht zwei kritische Operationen: (1) Die Projektion der DINOv2-Bildfeatures auf die Scalp-UV-Map (man muss wissen, welcher Bildbereich welchem Kopfhautpunkt entspricht), und (2) die Definition der Follicle-Positionen in 3D (die festen UV-Positionen werden über die rekonstruierte Geometrie in den 3D-Raum transformiert). Wenn das Fitting ungenau ist – z.B. die Kopfgröße oder -neigung nicht stimmt – werden die Features falsch auf die UV-Map projiziert: Haarinformation von der Stirn landet vielleicht an der falschen UV-Position. Die generierten Strähnen würden dann an falschen Stellen beginnen oder physikalisch unplausible Verläufe zeigen. Deshalb nutzen moderne Fitting-Methoden wie MICA oder DECA robuste Feature-basierte Schätzungen statt klassischer Landmark-basierter Optimierung."
                        }
                    ]
                },
                {
                    "type": "tutorial",
                    "title": "UV Mapping Grundlagen in Blender",
                    "authors": [],
                    "publisher": "Blender Documentation",
                    "year": 2024,
                    "url": "https://docs.blender.org/manual/en/latest/modeling/meshes/uv/index.html",
                    "priority": "recommended",
                    "estimated_hours": 1.5,
                    "reason": "Praktisches Verständnis von UV-Mapping hilft enorm, die Scalp-UV-Domäne intuitiv zu begreifen. Am besten lernst du UV-Mapping, indem du es einmal hands-on an einem einfachen Mesh ausprobierst.",
                    "recommended_sections": [
                        {
                            "name": "UV Mapping Einführung",
                            "focus": "Verstehe das Konzept: 3D-Oberfläche → 2D-Ebene auffalten",
                            "verified": false
                        },
                        {
                            "name": "UV Unwrapping",
                            "focus": "Probiere verschiedene Unwrapping-Methoden an einem einfachen Objekt aus",
                            "verified": false
                        }
                    ],
                    "takeaways": [
                        "UV-Mapping ist die Zuordnung von 2D-Koordinaten zu Punkten auf einer 3D-Oberfläche",
                        "Verschiedene Unwrapping-Methoden erzeugen verschiedene Verzerrungsmuster",
                        "Die UV-Map definiert einen kanonischen 2D-Raum, in dem man textur- oder featureartig arbeiten kann"
                    ],
                    "practical_exercises": [
                        "Erstelle ein einfaches Mesh in Blender und unwrappe es. Bemale die UV-Map und beobachte, wie sich die Bemalung auf dem 3D-Objekt verhält",
                        "Importiere ein FLAME-Mesh in Blender und inspiziere dessen UV-Layout"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Warum erzeugt UV-Unwrapping zwangsläufig Verzerrungen, und welche Konsequenz hat das für die Scalp-UV-Repräsentation?",
                            "answer": "Aus demselben Grund, warum eine Weltkarte die Erde verzerrt darstellt: Eine gekrümmte Oberfläche kann nicht verzerrungsfrei in die 2D-Ebene abgebildet werden (Theorema Egregium von Gauß). Für die Scalp-UV-Map bedeutet das: Gleich große Bereiche auf der Kopfhaut haben nicht zwangsläufig gleich große Bereiche in der UV-Map. Regionen, die in der UV-Map gestaucht sind, haben eine höhere Follikel-Dichte pro UV-Fläche. SAFE-Hair verwendet allerdings eine feste Menge von 32.768 Follikeln, die gleichmäßig im UV-Raum verteilt sind – die resultierende 3D-Verteilung wird durch das UV-Layout beeinflusst, was bei der Dekodierung berücksichtigt werden muss."
                        },
                        {
                            "question": "Was ist der Zusammenhang zwischen UV-Koordinaten und dem kanonischen Raum in SAFE-Hair?",
                            "answer": "In SAFE-Hair definiert die UV-Parametrisierung der FLAME-Kopfhaut einen kanonischen Raum, in dem alle Subjekte verglichen werden können. Weil FLAME eine feste Topologie hat, ist die UV-Map identisch für alle Identitäten. Eine UV-Koordinate (u,v) bezeichnet immer denselben semantischen Ort auf der Kopfhaut – z.B. 'links oben am Scheitel'. SAFE-Hair definiert Follikel als feste Punkte in diesem UV-Raum. Das Rectified-Flow-Modell arbeitet ebenfalls in diesem kanonischen UV-Raum: Es generiert 'Scalp Fields' – 2D-Karten über den UV-Koordinaten, die Occupancy und Strangrichtungen kodieren. Der kanonische Raum ermöglicht es, einen einzigen Generator für alle Identitäten zu trainieren, weil die Kopfhaut-Geometrie normalisiert ist."
                        },
                        {
                            "question": "Welche Informationen gehen beim Übergang vom 3D-Bildraum in den 2D-UV-Raum verloren, und wie kompensiert SAFE-Hair das?",
                            "answer": "Beim Projizieren der Bildfeatures auf die Scalp-UV-Map gehen zwei Arten von Information verloren: (1) Tiefe/Volumen – die UV-Map repräsentiert nur die Kopfhautoberfläche, nicht den Raum über ihr, in dem sich Haare bewegen. (2) Verdeckte Regionen – der Hinterkopf ist in einem Frontalporträt nicht sichtbar und hat keine projizierten Features. SAFE-Hair kompensiert beides: Die fehlende Volumeninformation wird durch die Strand-Dekodierung wiederhergestellt, die aus den 2D-Scalp-Fields 3D-Strangverläufe rekonstruiert (Segmentrichtungen + Länge → 3D-Kurve durch Forward-Integration). Die fehlenden Hinterkopf-Features werden durch das Rectified-Flow-Modell kompensiert, das gelernt hat, aus partiellen Scalp-Feature-Maps vollständige Fields zu generieren – es 'halluziniert' plausible Haarstrukturen für nicht sichtbare Regionen basierend auf gelernten Priors über Frisuren."
                        }
                    ]
                }
            ],
            "milestone": "Du kannst erklären, wie FLAME einen 3D-Kopf parametrisiert, was UV-Mapping ist und warum eine kanonische Scalp-UV-Domäne ein cleveres Designprinzip für haarverankertes Arbeiten ist. Du hast FLAME in PyTorch geladen und die UV-Map visualisiert."
        },
        {
            "phase": 3,
            "title": "Generative Modelle: Von Diffusion zu Rectified Flow",
            "description": "Das Herzstück von SAFE-Hair ist ein conditional Rectified Flow Modell, das aus verrauschten Initialisierungen vollständige Scalp Fields generiert. Rectified Flow ist eine Weiterentwicklung von Diffusion Models und Flow Matching. Du brauchst ein solides Verständnis dieser Konzepte, um die Generierung in SAFE-Hair nachzuvollziehen.",
            "resources": [
                {
                    "type": "blog",
                    "title": "What are Diffusion Models?",
                    "authors": [
                        "Lilian Weng"
                    ],
                    "publisher": "Lil'Log (OpenAI)",
                    "year": 2021,
                    "url": "https://lilianweng.github.io/posts/2021-07-11-diffusion-models/",
                    "priority": "essential",
                    "estimated_hours": 3,
                    "reason": "Lilian Wengs Blog ist der Gold-Standard für verständliche Erklärungen komplexer ML-Konzepte. Dieser Post baut das Verständnis von Diffusion Models von Grund auf, und du brauchst dieses Fundament, um Flow Matching und Rectified Flow einordnen zu können.",
                    "recommended_sections": [
                        {
                            "name": "Forward Diffusion Process",
                            "focus": "Verstehe, wie schrittweise Rauschen hinzugefügt wird und warum man das in geschlossener Form berechnen kann",
                            "verified": false
                        },
                        {
                            "name": "Reverse Process und Training Objective",
                            "focus": "Der Kern: Wie lernt man, Rauschen zu entfernen? Verstehe die ELBO-Herleitung und den vereinfachten Loss",
                            "verified": false
                        },
                        {
                            "name": "Score-Based Models",
                            "focus": "Der Übergang von diskreten Schritten zu kontinuierlichen SDEs – bereitet dich auf Flow Matching vor",
                            "verified": false
                        }
                    ],
                    "takeaways": [
                        "Diffusion = Forward Process (Rauschen hinzufügen) + Reverse Process (Rauschen entfernen)",
                        "Training: Modell lernt, den hinzugefügten Rauschanteil vorherzusagen (ε-prediction)",
                        "Score-basierte Perspektive: Man kann Diffusion als kontinuierliche SDE formulieren",
                        "Sampling erfordert viele Schritte (typisch 50-1000), was langsam ist"
                    ],
                    "practical_exercises": [
                        "Implementiere einen einfachen 2D-Diffusion-Process: Starte mit Punkten aus einer Spiralverteilung, füge schrittweise Rauschen hinzu und trainiere ein kleines Netzwerk, das den Reverse Process lernt",
                        "Visualisiere die Forward- und Reverse-Trajektorien – beobachte, wie gekrümmt sie sind (das wird beim Vergleich mit Rectified Flow wichtig)"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Warum sind die Sampling-Trajektorien bei Standard-Diffusion-Models typischerweise gekrümmt, und welches Problem erzeugt das?",
                            "answer": "Bei Standard-Diffusion-Models folgen die Sampling-Trajektorien einer stochastischen Differentialgleichung (SDE), die durch den gelernten Score (Gradienten der Log-Likelihood) gesteuert wird. Diese Trajektorien sind gekrümmt, weil der Score sich entlang des Weges ändert – in der Nähe der Datenverteilung zeigt er in andere Richtungen als in der Nähe der Rauschverteilung. Gekrümmte Trajektorien sind problematisch für schnelles Sampling: Wenn man mit wenigen Schritten (z.B. 1-4 statt 50-1000) samplen will, muss man die Kurve gut approximieren. Mit großen Schrittweiten 'schneidet' man Kurven ab und erzeugt Fehler. Das motiviert Rectified Flow: Wenn die Trajektorien gerade Linien wären, könnte man mit einem einzigen Schritt exakt samplen."
                        },
                        {
                            "question": "Was ist der konzeptionelle Unterschied zwischen dem Vorhersagen von Rauschen (ε-prediction) und dem Vorhersagen eines Vektorfeldes (wie bei Flow Matching)?",
                            "answer": "Bei ε-prediction lernt das Netzwerk für einen verrauschten Datenpunkt x_t vorherzusagen, welches Rauschen ε hinzugefügt wurde: x_t = √(ᾱ_t) · x_0 + √(1-ᾱ_t) · ε. Das Netzwerk approximiert also die 'Rauschkomponente'. Bei Flow Matching lernt das Netzwerk stattdessen ein Geschwindigkeitsfeld v(x_t, t), das die Richtung angibt, in die sich ein Punkt x_t zum Zeitpunkt t bewegen soll. Man kann zeigen, dass beides mathematisch äquivalent ist (man kann v und ε ineinander umrechnen), aber die Vektorfeld-Perspektive ist konzeptionell klarer: Man lernt direkt den Transport von Rausch- zur Datenverteilung als ODE dx/dt = v(x,t), ohne den Umweg über Noise-Schedules und Score-Funktionen."
                        },
                        {
                            "question": "Warum reicht ein einfaches Diffusion Model nicht für SAFE-Hair aus – was macht die Haardomäne besonders herausfordernd für generative Modelle?",
                            "answer": "Haarsträhnen haben mehrere Eigenschaften, die Standard-Diffusion-Models herausfordern: (1) Strukturierte Abhängigkeiten: Benachbarte Strähnen sind nicht unabhängig – sie müssen kohärente Muster bilden (Scheitel, Fließrichtung). (2) Physikalische Constraints: Strähnen müssen an der Kopfhaut starten, dürfen den Kopf nicht durchdringen und sollten physikalisch plausible Biegungen zeigen. (3) Multimodalität: Ein einziges Porträtfoto erlaubt viele plausible Hinterkopf-Frisuren. (4) Hohe Dimensionalität: 32.768 Strähnen × 32 Kontrollpunkte × 3 Koordinaten. SAFE-Hair adressiert das durch die Kombination aus kanonischem UV-Raum (erzwingt Kopfhautverankerung), Rectified Flow (effizientes Sampling der multimodalen Verteilung) und physikbasierte Validity Priors (Attachment, Collision, Bending Constraints als Post-Processing)."
                        }
                    ]
                },
                {
                    "type": "blog",
                    "title": "An Introduction to Flow Matching",
                    "authors": [
                        "Cambridge Machine Learning Group"
                    ],
                    "publisher": "Cambridge MLG Blog",
                    "year": 2024,
                    "url": "https://mlg.eng.cam.ac.uk/blog/2024/01/20/flow-matching.html",
                    "priority": "essential",
                    "estimated_hours": 2,
                    "reason": "Dieser Blogpost der Cambridge ML Group erklärt Flow Matching als Brücke zwischen Diffusion Models und Continuous Normalizing Flows. Er ist didaktisch gut aufgebaut und baut auf dem Diffusion-Verständnis auf, das du aus dem vorherigen Schritt hast.",
                    "recommended_sections": [
                        {
                            "name": "Von CNFs zu Flow Matching",
                            "focus": "Verstehe, warum klassische CNFs teuer zu trainieren sind und wie Flow Matching das löst",
                            "verified": false
                        },
                        {
                            "name": "Conditional Flow Matching",
                            "focus": "Der Kernalgorithmus: Training mit bedingten Vektorfeldern, die einzelne Datenpunkte erzeugen",
                            "verified": false
                        }
                    ],
                    "takeaways": [
                        "Flow Matching lernt ein Vektorfeld v(x,t), das Rausch- zur Datenverteilung transportiert",
                        "Training ist simulationsfrei: Man braucht keine ODE zu lösen während des Trainings",
                        "Conditional Flow Matching: Regrediere auf bedingte Geschwindigkeiten, die einzelne Datenpunkte generieren – das Ergebnis generiert die volle Verteilung",
                        "Mathematisch eleganter und flexibler als klassische Diffusion-Formulierungen"
                    ],
                    "practical_exercises": [
                        "Implementiere Flow Matching auf dem 2D-Spiraldatensatz aus der vorherigen Übung und vergleiche die Trajektorien mit denen des Diffusion-Models",
                        "Experimentiere mit der Anzahl der ODE-Solver-Schritte beim Sampling: Wie wenige Schritte brauchst du für akzeptable Ergebnisse?"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Was ist der zentrale Trick von Conditional Flow Matching, und warum macht er das Training so einfach?",
                            "answer": "Der zentrale Trick ist die Zerlegung des Problems: Statt direkt das marginale Vektorfeld zu lernen, das die gesamte Datenverteilung erzeugt (was erfordern würde, die Verteilung explizit zu kennen), lernt man bedingte Vektorfelder, die jeweils nur einen einzelnen Datenpunkt generieren. Für einen zufälligen Datenpunkt x_1 definiert man den bedingten Flow als lineare Interpolation: x_t = (1-t)·x_0 + t·x_1 (mit x_0 ~ Rauschen). Das bedingte Vektorfeld ist dann einfach v(x_t|x_1) = x_1 - x_0 – eine Konstante! Man trainiert ein Netzwerk, das bei gegebenem x_t und t dieses bedingte Vektorfeld vorhersagt. Man kann beweisen, dass das resultierende gelernte Feld das korrekte marginale Vektorfeld approximiert. Der Trainings-Loss ist ein simpler MSE, keine ELBO-Herleitung nötig."
                        },
                        {
                            "question": "Wie verbindet sich Flow Matching konzeptionell mit Optimalem Transport?",
                            "answer": "Flow Matching mit linearen Interpolationspfaden approximiert den optimalen Transport zwischen Rausch- und Datenverteilung. Optimaler Transport sucht die 'günstigste' Art, eine Verteilung in eine andere zu transformieren (minimaler Gesamtweg). Gerade Linien zwischen gepaarten Punkten (x_0, x_1) sind im Einzel-Paar-Fall optimal. Conditional Flow Matching erzwingt genau solche geraden Pfade für jedes Paar. Im marginalen Fall – wenn viele Pfade überlagert werden – können sich Pfade kreuzen, was zu nicht-geraden marginalen Trajektorien führt. Rectified Flow geht einen Schritt weiter und 'begradigt' auch die marginalen Trajektorien durch iteratives Reflow, was Few-Step-Sampling ermöglicht."
                        },
                        {
                            "question": "In SAFE-Hair transportiert das Rectified Flow Modell Gaussian Noise zu Scalp Fields. Was ist ein 'Scalp Field' konkret, und warum ist Flow Matching dafür besser geeignet als ein Standard-Diffusion-Modell?",
                            "answer": "Ein Scalp Field ist eine 2D-Map über den Scalp-UV-Koordinaten, die pro Follikel-Position mehrere Kanäle kodiert: (1) Occupancy (Wahrscheinlichkeit, dass dort ein Haar wächst), (2) Segment-Richtungen (Tangentenvektor für jeden der 32 Strangabschnitte), (3) Length Allocation (wie viel der Gesamtlänge auf welches Segment entfällt), (4) Gesamtlänge des Strangs. Flow Matching / Rectified Flow ist besser geeignet als Standard-Diffusion, weil: (a) Die geraden Trajektorien ermöglichen Sampling in wenigen Schritten (SAFE-Hair braucht nur 4.2 Sekunden pro Portrait), (b) der deterministische ODE-Solver produziert konsistentere Ergebnisse als stochastisches SDE-Sampling, und (c) Conditional Flow Matching integriert die DINOv2-Scalp-Features elegant als Conditioning – das Vektorfeld wird bedingt auf die projizierten Bildfeatures gelernt."
                        }
                    ]
                },
                {
                    "type": "blog",
                    "title": "Rectified Flow: Straight is Fast – Introduction",
                    "authors": [
                        "Rectified Flow Team"
                    ],
                    "publisher": "rectifiedflow.github.io",
                    "year": 2024,
                    "url": "https://rectifiedflow.github.io/blog/2024/intro/",
                    "priority": "essential",
                    "estimated_hours": 1.5,
                    "reason": "Die offizielle Tutorial-Serie der Rectified-Flow-Autoren erklärt den Übergang von Flow Matching zu Rectified Flow. Das ist direkt das generative Modell, das SAFE-Hair verwendet.",
                    "recommended_sections": [
                        {
                            "name": "Why Straight Flows Matter",
                            "focus": "Verstehe den Zusammenhang zwischen Geradheit der Trajektorien und Sampling-Effizienz",
                            "verified": false
                        },
                        {
                            "name": "Reflow Procedure",
                            "focus": "Wie man aus einem trainierten Flow-Modell durch iteratives 'Begradigen' ein effizienteres Modell macht",
                            "verified": false
                        }
                    ],
                    "takeaways": [
                        "Rectified Flow lernt gerade Transportpfade von Rausch- zu Datenverteilung",
                        "Geradere Pfade = weniger ODE-Solver-Schritte beim Sampling nötig",
                        "Reflow: Iteratives Verfahren, um Trajektorien weiter zu begradigen",
                        "Ermöglicht One-Step oder Few-Step Generation bei hoher Qualität"
                    ],
                    "practical_exercises": [
                        "Vergleiche die gelernten Trajektorien von Flow Matching und Rectified Flow visuell auf deinem 2D-Datensatz",
                        "Messe die Sampling-Qualität (z.B. FID auf einem einfachen Bilddatensatz) bei verschiedenen Schrittzahlen: 1, 2, 4, 8, 16 Schritte"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Was genau ist 'Reflow' und warum erzeugt es geradere Trajektorien?",
                            "answer": "Reflow ist ein iteratives Verfahren: Man trainiert zunächst ein Flow-Matching-Modell, generiert dann damit Datenpunkte (indem man Rauschen durch die gelernte ODE transportiert) und erhält so neue Paare (x_0, x_1), wobei x_0 das Startrauschen und x_1 der erzeugte Datenpunkt ist. Diese neuen Paare haben eine entscheidende Eigenschaft: Sie sind 'kausal gepaart' – x_0 und x_1 sind durch die gelernte ODE verbunden, nicht zufällig gepaart. Wenn man nun ein neues Flow-Modell auf diesen kausal gepaarten Daten trainiert, werden die Trajektorien gerader, weil die Paarung die Pfadkreuzungen reduziert, die entstehen, wenn Rauschpunkte 'falsch' mit Datenpunkten gepaart sind. Man kann Reflow mehrfach wiederholen, um die Trajektorien weiter zu begradigen."
                        },
                        {
                            "question": "Warum ist SAFE-Hair auf schnelles Sampling angewiesen, und was wäre die Alternative?",
                            "answer": "SAFE-Hair produziert ein Ergebnis in 4.2 Sekunden pro Portrait – schnell genug für interaktive Anwendungen in Produktions-Pipelines (z.B. ein Artist erstellt mehrere Varianten einer Frisur). Ohne Rectified Flow und mit einem Standard-Diffusion-Modell, das 50-100 Sampling-Schritte bräuchte, läge die Inferenzzeit deutlich höher (vielleicht 30-60 Sekunden), was den interaktiven Workflow zerstören würde. Zudem erzeugen deterministische ODE-Pfade bei wenigen Schritten konsistentere Ergebnisse als stochastisches SDE-Sampling mit wenigen Schritten. Die Alternative wäre Distillation (z.B. Consistency Models), aber Rectified Flow erreicht die Effizienz ohne separaten Distillationsschritt."
                        },
                        {
                            "question": "Wie wird das Conditioning in SAFE-Hair's Rectified Flow realisiert – wie fließen die Bildinformationen in die Generierung ein?",
                            "answer": "SAFE-Hair's Rectified Flow ist ein conditional generatives Modell: Es generiert nicht zufällige Frisuren, sondern solche, die zum Eingabeporträt passen. Das Conditioning funktioniert über die auf die Scalp-UV-Map projizierten DINOv2-Features. Das Vektorfeld v(x_t, t, c) erhält neben dem aktuellen verrauschten Zustand x_t und dem Zeitschritt t auch die Conditioning-Features c als Eingabe. Konkret: Für sichtbare Kopfhautregionen liefern die projizierten DINOv2-Features starke Signale, die die Generierung direkt steuern (das Modell 'sieht' die Haarstruktur im Bild). Für nicht sichtbare Regionen fehlen diese Features (oder sind auf Hintergrund-Features gesetzt), und das Modell fällt auf gelernte Priors zurück – es generiert plausible Ergänzungen basierend auf dem, was es über Frisuren gelernt hat und den sichtbaren Teilen der Frisur."
                        }
                    ]
                }
            ],
            "milestone": "Du verstehst den Dreischritt Diffusion → Flow Matching → Rectified Flow und kannst erklären, warum SAFE-Hair Rectified Flow verwendet. Du kannst die Begriffe 'Vektorfeld', 'ODE-Transport', 'Conditional Flow Matching' und 'Reflow' in eigenen Worten erklären."
        },
        {
            "phase": 4,
            "title": "Haarmodellierung und Prior Work",
            "description": "Jetzt hast du die ML-Grundlagen und kannst dich der Domäne widmen: Wie werden Haare in der Computergrafik repräsentiert? Welche Ansätze zur 3D-Haarrekonstruktion gab es vor SAFE-Hair? Diese Phase gibt dir den Kontext, um SAFE-Hair's Beiträge einzuordnen.",
            "resources": [
                {
                    "type": "paper",
                    "title": "Perm: A Parametric Representation for Multi-Style 3D Hair Modeling",
                    "authors": [
                        "Chengan He",
                        "Xin Sun",
                        "Zhixin Shu",
                        "Fujun Luan",
                        "Sören Pirk",
                        "Jorge Alejandro Amador Herrera",
                        "Dominik L. Michels",
                        "Tuanfeng Y. Wang"
                    ],
                    "publisher": "ICLR",
                    "year": 2025,
                    "url": "https://github.com/c-he/perm",
                    "priority": "essential",
                    "estimated_hours": 3,
                    "reason": "Perm ist eine direkte Vorgängerarbeit zu SAFE-Hair und definiert viele der Repräsentationskonzepte (parametrische Strangkodierung, Follikel-basierte Generierung), die SAFE-Hair weiterentwickelt. Zudem ist der Code öffentlich, was dir hands-on Zugang zur Domäne gibt.",
                    "recommended_sections": [
                        {
                            "name": "Strand Representation",
                            "focus": "Wie werden einzelne Haarsträhnen mathematisch dargestellt? Kontrollpunkte, Tangenten, Längen.",
                            "verified": false
                        },
                        {
                            "name": "Scalp Parameterization",
                            "focus": "Wie werden Haarwurzeln auf der Kopfhaut parametrisiert?",
                            "verified": false
                        },
                        {
                            "name": "Generation and Editing",
                            "focus": "Wie kann man generierte Haare editieren? Das ist der Praxisvorteil, den auch SAFE-Hair anstrebt.",
                            "verified": false
                        }
                    ],
                    "takeaways": [
                        "Strand-basierte Repräsentation: Jedes Haar ist eine 3D-Kurve mit Kontrollpunkten",
                        "Parametrische Kodierung ermöglicht kompakte Darstellung und Editierbarkeit",
                        "Die Verbindung von Follikel-Position und Stranggeometrie ist zentral",
                        "Export in Produktionsformate (Alembic) ist ein wichtiges Praxisziel"
                    ],
                    "practical_exercises": [
                        "Klone das Perm-Repository und führe die Demo-Inferenz aus: Generiere 3D-Haare aus dem Modell und visualisiere sie",
                        "Experimentiere mit dem Editing: Wie verändert sich die Frisur, wenn du Parameter variierst?",
                        "Exportiere ein generiertes Haarmodell in Alembic und lade es in Blender"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Warum ist eine strand-basierte Repräsentation (explizite 3D-Kurven) für Produktionsanwendungen besser geeignet als eine volumetrische Repräsentation (z.B. NeRF oder 3D-Gaussians)?",
                            "answer": "In Produktions-Pipelines (Film, Games, VFX) werden Haare physikalisch simuliert (Wind, Schwerkraft, Kollisionen), gestylt (Bürste, Kamm, Gel-Effekte), gerendert (mit Strand-spezifischen Shading-Modellen wie Marschner oder d'Eon) und in Standard-Formaten wie Alembic (.abc) zwischen Tools ausgetauscht. All das erfordert explizite Stranggeometrie: Eine Simulation braucht diskrete Massenpunkte entlang jeder Strähne, ein Shader braucht Tangentenvektoren, Export braucht Vertex-Positionen. Volumetrische Repräsentationen wie NeRFs oder 3D-Gaussians können Haare zwar rendern, aber nicht simulieren oder in Standard-Produktions-Pipelines exportieren. Sie kodieren Appearance (wie sehen Haare aus?) statt Geometry (wo verlaufen die Strähnen?). SAFE-Hair erzeugt deshalb 'exportierbare' – also explizit strand-basierte – Ergebnisse."
                        },
                        {
                            "question": "Was ist der Unterschied zwischen 'Guide Strands' und einem vollständigen 'Groom', und warum verwendet SAFE-Hair 32.768 Strähnen statt z.B. 100.000?",
                            "answer": "In der Produktionspraxis unterscheidet man Guide Strands (wenige hundert bis tausend Leitsträhnen, die die grobe Frisurform definieren) und den finalen Groom (volle Dichte, oft 50.000-150.000 Strähnen für einen realistischen Kopf). Guide Strands werden manuell oder prozedural platziert, und der volle Groom wird durch Interpolation zwischen Guides erzeugt. SAFE-Hair generiert 32.768 Strähnen – das liegt zwischen einem Guide-Set und einem vollen Groom. Es ist dicht genug, um die Frisur vollständig zu definieren (kein weiteres Upsampling nötig für die Silhouette), aber nicht so dicht, dass es die Generierung übermäßig verlangsamt. SAFE-Hair gruppiert seine Strähnen zudem in Guide Families – Cluster, die in Produktionstools als interaktive Einheiten dienen."
                        },
                        {
                            "question": "Welche Herausforderung stellt die Rückseite des Kopfes (nicht sichtbar im Frontalporträt) für die Haarrekonstruktion dar, und wie löst Perm das im Vergleich zu SAFE-Hair?",
                            "answer": "Die Hinterkopf-Herausforderung ist das 'Ill-Posed-Problem' der Single-View-Rekonstruktion: Aus einem Frontalporträt kann man die Frisur am Hinterkopf nicht direkt sehen – es gibt unendlich viele plausible Fortsetzungen. Perm löst das durch eine parametrische Repräsentation, die auf einem großen Datensatz von 3D-Frisuren trainiert wurde: Das Modell hat globale Frisur-Priors gelernt (z.B. 'Bob-Frisuren haben am Hinterkopf diese Form') und generiert den Hinterkopf basierend auf dem gelernten latenten Raum. SAFE-Hair geht einen Schritt weiter durch die Scalp-UV-Domäne und das Rectified-Flow-Modell: Es modelliert die Verteilung plausibler Scalp Fields direkt im kanonischen UV-Raum, was eine natürlichere Completion ermöglicht, weil die Generierung die räumliche Struktur der Kopfhaut respektiert und die sichtbaren Features als starkes Conditioning nutzt."
                        }
                    ]
                },
                {
                    "type": "repository",
                    "title": "USC-HairSalon Dataset",
                    "authors": [
                        "Liwen Hu et al."
                    ],
                    "publisher": "USC",
                    "year": 2015,
                    "url": "http://www-scf.usc.edu/~liwenhu/SHM/database.html",
                    "priority": "recommended",
                    "estimated_hours": 1,
                    "reason": "Der Standard-Datensatz für 3D-Haarmodellierung. Er wird in nahezu allen Arbeiten der Domäne verwendet, auch als Grundlage für SAFE-Hair's Training. Verschafft dir ein Gefühl für die Daten.",
                    "recommended_sections": [
                        {
                            "name": "Dataset Overview",
                            "focus": "Verstehe die Struktur: 343 Frisuren, je 10.000 Strähnen, 100 Kontrollpunkte pro Strähne",
                            "verified": false
                        }
                    ],
                    "takeaways": [
                        "Standard-Benchmark-Datensatz mit fester Topologie (alle Frisuren auf demselben Kopfmodell ausgerichtet)",
                        "10.000 Strähnen pro Frisur mit bis zu 100 Vertices pro Strähne",
                        "Dateiformat: .data-Dateien mit Vertex-Positionen"
                    ],
                    "practical_exercises": [
                        "Lade einige Frisuren herunter und visualisiere sie in Python (matplotlib 3D oder Open3D)",
                        "Analysiere die Statistik: Verteilung der Stranglängen, Kurvatur, Root-Positionen auf der Kopfhaut"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Warum sind 343 Frisuren (USC-HairSalon) als Trainingsdaten für ein neuronales Modell eigentlich viel zu wenig, und wie löst die Forschung das?",
                            "answer": "343 Frisuren sind für Deep Learning extrem wenig – zum Vergleich hat ImageNet über 1 Million Bilder. Die Forschung löst das mit mehreren Strategien: (1) Data Augmentation – der Hair20k-Datensatz erweitert USC-HairSalon auf 21.054 Frisuren durch geometrische Augmentierungen (Rotation, Spiegelung, lokale Verformungen). (2) Synthetisches Rendering – 3D-Frisuren werden aus vielen Blickwinkeln mit verschiedenen Beleuchtungen gerendert, was Tausende von 2D-3D-Paarungen ergibt. (3) Priors aus Bildmodellen – SAFE-Hair nutzt DINOv2-Features, die auf Millionen von Bildern vortrainiert sind. (4) SAFE-Hair's HairBench-3D sammelt zusätzliche öffentliche 3D-Hair-Assets mit standardisierter Ausrichtung und Metriken. Die Kombination aus wenigen 3D-Daten mit starken 2D-Priors ist ein Schlüsseldesign moderner Methoden."
                        },
                        {
                            "question": "Was bedeutet 'feste Topologie' bei den USC-HairSalon-Daten, und wie profitiert SAFE-Hair davon?",
                            "answer": "Feste Topologie bedeutet, dass alle 343 Frisuren auf dasselbe Kopfmodell ausgerichtet sind: Gleiche Mesh-Vertices, gleiche Scalp-Region, gleiche Root-Verteilung. Das ermöglicht es, Frisuren direkt zu vergleichen (Vertex i der Frisur A vs. Vertex i der Frisur B), was supervised Training vereinfacht. SAFE-Hair profitiert davon doppelt: (1) Das Rectified-Flow-Modell kann im kanonischen Scalp-UV-Raum trainieren, weil alle Trainingsdaten in denselben Raum ausgerichtet sind. (2) Die Evalutions-Metriken (Chamfer Distance, F-Score) sind sinnvoll, weil der Referenzraum konsistent ist. Bei Inference überbrückt SAFE-Hair die Lücke zu realen Fotos durch FLAME-Fitting – es transformiert den rekonstruierten Kopf in den kanonischen Raum."
                        },
                        {
                            "question": "Warum reichen rein bildbasierte Metriken (PSNR, SSIM, LPIPS) nicht aus, um 3D-Haarrekonstruktionen zu evaluieren?",
                            "answer": "Bildbasierte Metriken vergleichen nur, wie die Haare aus bestimmten Blickwinkeln AUSSEHEN – nicht, wie sie geometrisch strukturiert sind. Zwei völlig verschiedene 3D-Strangkonfigurationen können aus einem Blickwinkel identisch gerendert werden, aber aus anderen Winkeln oder bei Simulation/Animation komplett unterschiedlich wirken. SAFE-Hair's HairBench-3D evaluiert deshalb mit 3D-Geometrie-Metriken: Chamfer Distance misst den durchschnittlichen Abstand zwischen rekonstruierten und Ground-Truth-Punkten, F-Score misst den Anteil korrekt rekonstruierter Punkte, Direction Consistency prüft ob die Tangentenvektoren stimmen, Root Validity prüft ob Strähnen wirklich auf der Kopfhaut starten (99.8%!), und Penetration Ratio misst wie viele Strähnen den Kopf durchdringen (nur 3.9%). Diese Metriken erfassen die Produktionstauglichkeit des Ergebnisses."
                        }
                    ]
                }
            ],
            "milestone": "Du verstehst strand-basierte Haarrepräsentationen, kennst die wichtigsten Datensätze und Prior Work, und kannst erklären, warum exportierbare Stranggeometrie der Schlüssel für Produktionsanwendungen ist."
        },
        {
            "phase": 5,
            "title": "SAFE-Hair im Detail: Paper, Code und Praxis",
            "description": "Jetzt hast du alle Bausteine und kannst SAFE-Hair vollständig durchdringen. In dieser Phase liest du das Paper gründlich, arbeitest mit dem Code und verstehst jede Komponente der Pipeline.",
            "resources": [
                {
                    "type": "paper",
                    "title": "SAFE-Hair: Scalp-Anchored Fields for Exportable Single-View Hair Reconstruction",
                    "authors": [
                        "SAFE-Hair Authors"
                    ],
                    "publisher": "NeurIPS",
                    "year": 2026,
                    "url": "https://arxiv.org/abs/2611.12037",
                    "priority": "essential",
                    "estimated_hours": 5,
                    "reason": "Das Kernpaper. Mit den vorherigen Phasen bist du bestens vorbereitet, um es im Detail zu lesen und zu verstehen. Lies es nicht nur einmal, sondern gehe es methodisch durch.",
                    "recommended_sections": [
                        {
                            "name": "Section 3: Method",
                            "focus": "Der Kern der Arbeit. Gehe jede Untersektion langsam durch: Scalp-UV Conditioning → Rectified Flow → Persistent Follicle Decoding → Validity Priors. Zeichne dir die Pipeline als Diagramm.",
                            "verified": true
                        },
                        {
                            "name": "Section 4: HairBench-3D",
                            "focus": "Verstehe, warum die Autoren einen neuen Benchmark brauchten und wie er aufgebaut ist",
                            "verified": true
                        },
                        {
                            "name": "Section 5: Experiments",
                            "focus": "Fokus auf die Vergleichstabellen und Ablation Studies – welche Komponenten tragen wie viel bei?",
                            "verified": true
                        },
                        {
                            "name": "Abstract und Section 1: Introduction",
                            "focus": "Lies das Abstract zuerst, dann die Einleitung – sie positioniert SAFE-Hair im Feld",
                            "verified": true
                        }
                    ],
                    "takeaways": [
                        "Die vollständige Pipeline: Bild → FLAME-Fitting → DINOv2-Feature-Extraktion → Scalp-UV-Projektion → Conditional Rectified Flow → Scalp Fields → Follicle Decoding → Validity Priors → Export",
                        "32.768 Strähnen mit je 32 Kontrollpunkten, in 4.2 Sekunden pro Portrait",
                        "HairBench-3D als neuer Evaluationsstandard mit Metriken für Geometrie, Richtungskonsistenz, Hinterkopf-Completion, Silhouette und Kollision",
                        "State-of-the-Art-Ergebnisse: 3.28mm Chamfer Distance, 81.7% F-Score, 99.8% Root Validity"
                    ],
                    "practical_exercises": [
                        "Zeichne die komplette SAFE-Hair-Pipeline als Blockdiagramm – von Eingabe bis Ausgabe, mit allen Zwischenrepräsentationen",
                        "Klone das offizielle Repository (github.com/SAFE-Hair/Code) und führe die Inferenz auf eigenen Porträtfotos aus",
                        "Inspiziere die generierten Alembic-Dateien in Blender: Prüfe Root-Attachment, Strangverläufe und Physikplausibilität",
                        "Führe die Evaluation auf HairBench-3D durch und reproduziere die Metriken aus dem Paper"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Erkläre die gesamte SAFE-Hair-Pipeline von Eingabebild bis zum exportierten Groom in deinen eigenen Worten. Was passiert in jedem Schritt, und welche Repräsentation hat das Zwischenergebnis?",
                            "answer": "Schritt 1 – FLAME-Fitting: Das Eingabeporträt wird analysiert, um ein FLAME-3D-Kopfmodell zu fitten. Ergebnis: 3D-Mesh mit bekannter Geometrie, Pose und Kameraparametern. Schritt 2 – Feature-Extraktion und Projektion: DINOv2 extrahiert Patch-Level-Features aus dem Bild. Über die bekannte 3D-Geometrie und Kamerapose werden diese Features auf die Scalp-UV-Map projiziert. Ergebnis: Eine 2D-Feature-Map über den UV-Koordinaten der Kopfhaut, wobei nicht sichtbare Regionen fehlende/leere Features haben. Schritt 3 – Conditional Rectified Flow: Ein Rectified-Flow-Modell nimmt Gaussian Noise als Input und die Feature-Map als Conditioning und transportiert das Rauschen durch eine gelernte ODE zu einem latenten Scalp Field. Der Flow füllt dabei auch die nicht sichtbaren Regionen mit plausiblen Werten. Ergebnis: Latentes Scalp Field über den gesamten UV-Raum. Schritt 4 – Persistent Follicle Decoding: An 32.768 festen Follikel-Positionen im UV-Raum dekodiert ein Shared Decoder aus dem Scalp Field: Occupancy (Haar ja/nein), Segment-Richtungen (32 Tangentenvektoren), Length Allocation (Verteilung der Länge auf Segmente) und Gesamtlänge. Die 3D-Strangkurve wird durch Forward-Integration der Tangentenrichtungen vom Root aus rekonstruiert. Ergebnis: 32.768 explizite 3D-Strangkurven mit je 32 Kontrollpunkten. Schritt 5 – Validity Priors: Attachment Constraints stellen sicher, dass Roots auf der Kopfhaut liegen, Collision Constraints verhindern Durchdringungen des Kopfmeshs, Bending Constraints begrenzen unrealistische Krümmungen. Ergebnis: Physikalisch plausibles Strang-Set. Schritt 6 – Export: Die Strähnen werden in Guide Families geclustert und im Alembic-Format (.abc) serialisiert, bereit für Blender, Houdini oder Unreal Engine."
                        },
                        {
                            "question": "Was genau kodiert ein 'Scalp Field' und warum ist diese Repräsentation besser als direkte 3D-Koordinaten-Vorhersage?",
                            "answer": "Ein Scalp Field ist eine Multi-Channel-2D-Map über dem kanonischen Scalp-UV-Raum mit folgenden Kanälen pro Follikel: (1) Occupancy: Skalarwert [0,1] – soll dort ein Haar wachsen? (2) Segment Directions: 32 × 3D-Tangentenvektoren, die die Wuchsrichtung jedes Strangsegments angeben. (3) Length Allocation: 32 Werte, die bestimmen, wie viel der Gesamtlänge auf jedes Segment entfällt. (4) Total Length: Gesamtlänge des Strangs. Diese Repräsentation ist besser als direkte 3D-Koordinaten-Vorhersage aus mehreren Gründen: (a) Die Zerlegung in Richtung + Länge ist physikalisch motiviert – Haare wachsen von der Wurzel und folgen einer Richtung. (b) Die Tangentenrichtungen sind lokal definiert und haben begrenzte Wertebereiche (Einheitsvektoren), was die Generierung einfacher macht als die Vorhersage absoluter 3D-Koordinaten, die stark vom Kopfmodell abhängen. (c) Die 2D-UV-Struktur ermöglicht es dem Rectified-Flow-Modell, räumliche Korrelationen zwischen benachbarten Follikeln effizient zu modellieren (wie ein Bild-Generierungsmodell, das räumliche Kohärenz in 2D lernt)."
                        },
                        {
                            "question": "Welche Rolle spielen die Validity Priors und warum kann man sie nicht einfach weglassen? Was würde passieren?",
                            "answer": "Die Validity Priors sind physikbasierte Post-Processing-Constraints, die drei Arten von Artefakten korrigieren: (1) Attachment Constraint: Stellt sicher, dass die rekonstruierte Root-Position jedes Strangs tatsächlich auf der FLAME-Kopfhautoberfläche liegt. Ohne diesen Constraint könnten Strähnen 'in der Luft' beginnen – ein offensichtliches visuelles Artefakt und katastrophal für Simulation. (2) Collision Constraint: Verhindert, dass Strähnen durch den Kopf verlaufen. Ohne ihn penetrieren im Schnitt mehr Strähnen die Kopfgeometrie – der aktuelle Wert ist 3.9%, ohne Constraint wäre er deutlich höher. Penetrierende Strähnen sind in der Produktion nicht akzeptabel. (3) Bending Constraint: Begrenzt die maximale Krümmung pro Segment. Ohne ihn könnten einzelne Strähnen unnatürliche Knicke aufweisen, die physikalisch unmöglich sind. Man kann sie nicht weglassen, weil das Rectified-Flow-Modell in einem latenten Raum arbeitet und keine harten physikalischen Constraints erzwingen kann – es lernt 'soft' Priors aus den Trainingsdaten. Die Validity Priors sind ein elegantes Hybrid-Design: Neuronales Netz für die schwierige Generierung + explizite Regeln für die Physik."
                        }
                    ]
                },
                {
                    "type": "repository",
                    "title": "SAFE-Hair Official Code Repository",
                    "authors": [
                        "SAFE-Hair Team"
                    ],
                    "publisher": "GitHub",
                    "year": 2026,
                    "url": "https://github.com/SAFE-Hair/Code",
                    "priority": "essential",
                    "estimated_hours": 4,
                    "reason": "Der offizielle Code gibt dir die Möglichkeit, die Methode praktisch nachzuvollziehen und mit eigenen Daten zu experimentieren. Lies den Code parallel zum Paper.",
                    "recommended_sections": [
                        {
                            "name": "Inference Pipeline",
                            "focus": "Verfolge den Datenfluss von Bild-Input bis Alembic-Output im Code",
                            "verified": false
                        },
                        {
                            "name": "Model Architecture",
                            "focus": "Wie ist der Rectified-Flow-Backbone implementiert? Welches Netzwerk lernt das Vektorfeld?",
                            "verified": false
                        },
                        {
                            "name": "Scalp Field Decoding",
                            "focus": "Wie werden die Scalp Fields in diskrete Strangkurven umgewandelt?",
                            "verified": false
                        }
                    ],
                    "takeaways": [
                        "Praktisches Verständnis der gesamten Pipeline-Implementierung",
                        "Fähigkeit, die Methode auf eigenen Daten auszuführen",
                        "Verständnis der konkreten Netzwerkarchitekturen und Hyperparameter"
                    ],
                    "practical_exercises": [
                        "Führe die Inferenz auf 10 verschiedenen Porträtfotos aus und analysiere die Ergebnisse qualitativ: Welche Frisuren gelingen gut, welche weniger?",
                        "Modifiziere die Anzahl der Sampling-Schritte im Rectified Flow und beobachte den Qualitäts-Geschwindigkeits-Trade-off",
                        "Experimentiere mit dem Export: Lade die Alembic-Files in Blender, wende Hair-Simulation an, rendere die Haare mit einem Strand-Shader"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Welche Teile der Pipeline sind differenzierbar und welche nicht? Wo endet das 'Neuronale' und wo beginnt das 'Algorithmische'?",
                            "answer": "Differenzierbar (neuronale Komponenten): (1) DINOv2-Feature-Extraktion – vortrainierter ViT, frozen, aber differenzierbar. (2) Scalp-UV Feature Projection – differenzierbares Sampling via bilineare Interpolation. (3) Rectified Flow Netzwerk – das trainierte Vektorfeld, vollständig differenzierbar. (4) Follicle Decoder – das Netzwerk, das Occupancy, Richtungen und Längen vorhersagt. Nicht differenzierbar (algorithmisch): (1) FLAME-Fitting – typischerweise ein separater Optimierungsprozess. (2) Forward Integration der Strangkurven – numerische Integration der Tangentenvektoren, prinzipiell differenzierbar, aber in der Praxis als Post-Processing implementiert. (3) Validity Priors – Projektion auf Constraints (Attachment, Collision, Bending), nicht differenzierbar implementiert. (4) Alembic-Export – reine Serialisierung. Die Trennlinie zeigt ein Designprinzip: Neuronale Netze für die schwierige Generierung (wo Priors aus Daten gelernt werden müssen), explizite Algorithmen für physikalische Korrektheit (wo Regeln bekannt sind)."
                        },
                        {
                            "question": "SAFE-Hair erreicht 99.8% Root Validity. Was bedeutet diese Metrik genau, und warum ist sie fast perfekt?",
                            "answer": "Root Validity misst den Anteil der generierten Strähnen, deren Wurzelpunkt tatsächlich auf der Kopfhautoberfläche des FLAME-Modells liegt (innerhalb eines kleinen Toleranzabstands). 99.8% bedeutet, dass nur 0.2% der 32.768 Strähnen (etwa 65 Strähnen) einen Root haben, der nicht korrekt auf der Kopfhaut sitzt. Die Metrik ist fast perfekt, weil SAFE-Hair Root Validity BY DESIGN erzwingt – und zwar doppelt: (1) Die Follikel-Positionen sind als feste Punkte im Scalp-UV-Raum definiert und werden über die FLAME-Geometrie in 3D transformiert. Sie STARTEN per Definition auf der Kopfhaut. (2) Der Attachment Constraint in den Validity Priors korrigiert etwaige numerische Ungenauigkeiten. Die 0.2% Fehler kommen vermutlich von Edge Cases an der Grenze der Scalp-Region, wo die UV-Parametrisierung Unregelmäßigkeiten hat. Diese Design-Entscheidung (feste Follikel statt frei vorhergesagter Roots) ist einer der Schlüsselbeiträge von SAFE-Hair."
                        },
                        {
                            "question": "Wie unterscheidet sich SAFE-Hair fundamental von Methoden, die 3D-Gaussians oder NeRF für Haarrekonstruktion verwenden? Was sind die jeweiligen Stärken und Schwächen?",
                            "answer": "Der fundamentale Unterschied liegt in der Repräsentation: SAFE-Hair erzeugt EXPLIZITE Stranggeometrie (32.768 Kurven mit Kontrollpunkten), während NeRF/3DGS IMPLIZITE volumetrische Repräsentationen erzeugen (Dichtefeld bzw. Gaussians). Stärken von SAFE-Hair / Explizite Strähnen: (a) Direkt exportierbar in Produktions-Pipelines. (b) Physikalisch simulierbar (Wind, Schwerkraft). (c) Editierbar (Strähnen verschieben, kürzen, restylen). (d) Standard-Strand-Shader für fotorealistisches Rendering. (e) Funktioniert mit einem einzigen Bild. Schwächen: (a) Begrenzte Vielfalt der Texturen/Farben – Stranggeometrie enthält keine Farbinformation. (b) Braucht ein Template-Kopfmodell (FLAME). Stärken von NeRF/3DGS: (a) Fotorealistisches Appearance inklusive Farbe, Transparenz, Highlights. (b) Kein Template-Modell nötig. (c) Kann aus Multi-View-Input sehr detaillierte Ergebnisse liefern. Schwächen: (a) Nicht direkt exportierbar – Konversion zu Strähnen ist ein offenes Problem. (b) Nicht simulierbar. (c) Multi-View-Input meist nötig. Die Methoden ergänzen sich also: NeRF/3DGS für Rendering und View Synthesis, SAFE-Hair für Asset-Erstellung und Produktion."
                        }
                    ]
                }
            ],
            "milestone": "Du kannst SAFE-Hair vollständig erklären, hast die Inferenz auf eigenen Bildern ausgeführt und die Ergebnisse in Blender visualisiert. Du verstehst jede Komponente der Pipeline und kannst die Design-Entscheidungen begründen."
        },
        {
            "phase": 6,
            "title": "Aktuelle Forschung und offene Probleme",
            "description": "In dieser Phase ordnest du SAFE-Hair in das größere Forschungsfeld ein, lernst verwandte aktuelle Arbeiten kennen und identifizierst offene Probleme und Zukunftsrichtungen.",
            "resources": [
                {
                    "type": "paper",
                    "title": "HairLRM: Strand-based Hair Modeling via Large Reconstruction Models",
                    "authors": [],
                    "publisher": "arXiv",
                    "year": 2026,
                    "url": "https://arxiv.org/pdf/2606.15238",
                    "priority": "recommended",
                    "estimated_hours": 2,
                    "reason": "HairLRM verfolgt einen komplementären Ansatz: Statt Rectified Flow nutzt es Large Reconstruction Models (LRM-Architektur). Der Vergleich hilft dir, die Design-Entscheidungen von SAFE-Hair besser einzuordnen.",
                    "recommended_sections": [
                        {
                            "name": "Method Overview",
                            "focus": "Vergleiche den Ansatz mit SAFE-Hair: Welche Pipeline-Schritte unterscheiden sich?",
                            "verified": false
                        }
                    ],
                    "takeaways": [
                        "LRM-basierte Ansätze nutzen große Transformer-Modelle für direkte Rekonstruktion",
                        "Unterschiedlicher Trade-off: Weniger explizite Priors, dafür mehr gelernt",
                        "Vergleich der Ergebnisqualität und Export-Fähigkeit mit SAFE-Hair"
                    ],
                    "practical_exercises": [
                        "Erstelle eine Vergleichstabelle: SAFE-Hair vs. HairLRM vs. Perm – Repräsentation, Input, Output, Geschwindigkeit, Metriken"
                    ],
                    "understanding_questions": [
                        {
                            "question": "Welche offenen Probleme in der Single-View Hair Reconstruction sind noch ungelöst, und was wäre nötig, um sie zu lösen?",
                            "answer": "Mehrere fundamentale Herausforderungen bleiben: (1) Haarfarbe und Textur: SAFE-Hair rekonstruiert nur Geometrie, nicht Farbe. Eine vollständige Lösung bräuchte eine zusätzliche Appearance-Vorhersage pro Strang (Melanin-Verteilung, Transparenz). (2) Extreme Frisuren: Zöpfe, Dreadlocks, hochgesteckte Frisuren haben topologisch komplexe Strukturen, die sich schlecht als unabhängige Strähnen modellieren lassen. (3) Haarschmuck und Accessoires: Clips, Bänder, Mützen interagieren mit der Haargeometrie und sind nicht im Modell. (4) Dynamik: Ein Einzelbild enthält keine Dynamik-Information – für physikalisch plausible Simulation bräuchte man materialspezifische Parameter (Steifigkeit, Masse). (5) Konsistenz über Videos: Frame-für-Frame-Rekonstruktion erzeugt zeitliches Flimmern – temporale Kohärenz ist ein offenes Problem. (6) Diversität der Trainingsdaten: Die meisten Datensätze sind auf bestimmte Haartypen beschränkt – lockiges, afro-texturiertes Haar ist unterrepräsentiert."
                        },
                        {
                            "question": "Wie könnte SAFE-Hair mit einem 3D-Gaussian-Splatting-basierten Ansatz kombiniert werden, und welchen Mehrwert hätte das?",
                            "answer": "Eine hybride Pipeline könnte die Stärken beider Ansätze vereinen: SAFE-Hair liefert die explizite Stranggeometrie (exportierbar, simulierbar), während 3DGS die fotorealistische Appearance liefert (Farbe, Transparenz, Specular). Konkret: (1) SAFE-Hair rekonstruiert die Stranggeometrie aus dem Porträt. (2) Entlang jeder Strähne werden 3D-Gaussians platziert, deren Positionen durch die Strangkurve definiert sind. (3) Die Gaussian-Parameter (Farbe, Opazität, Covariance) werden optimiert, um das Eingabebild zu reproduzieren. Das Ergebnis wäre ein Asset, das sowohl geometrisch korrekt (simulierbar, exportierbar) als auch visuell fotorealistisch ist. Die Strangstruktur würde als 'Skelett' für die Gaussians dienen und physikalische Plausibilität erzwingen, während die Gaussians die visuelle Qualität liefern, die reine Strang-Rendering-Methoden nicht erreichen."
                        },
                        {
                            "question": "Welche Rolle spielt die Wahl des kanonischen Raums (Scalp-UV) im Vergleich zu alternativen kanonischen Räumen, und gibt es bessere Optionen?",
                            "answer": "Die Scalp-UV-Parametrisierung ist eine spezifische Design-Entscheidung mit klaren Trade-offs. Vorteile: Strähnen sind BY DESIGN an der Kopfhaut verankert, die 2D-Struktur ermöglicht effiziente Convolutions/Attention, und das feste Follikel-Set gibt jedem Strang eine konsistente Identität. Nachteile: UV-Verzerrungen beeinflussen die Follikel-Verteilung, die 2D-Map kann den 3D-Raum über der Kopfhaut nur indirekt kodieren, und extreme Frisuren (z.B. Pferdeschwanz, der weit vom Kopf absteht) sind schwer als 'Scalp Field' zu repräsentieren. Alternativen: (1) Volumetrischer kanonischer Raum (3D-Grid um den Kopf) – flexibler für extreme Frisuren, aber rechenaufwändiger. (2) Sphärischer Harmonic Space – kompaktere Darstellung globaler Frisurform, aber weniger lokal. (3) Impliziter kanonischer Raum (gelernter latenter Raum) – maximale Flexibilität, aber schwieriger zu interpretieren und zu exportieren. SAFE-Hair's Wahl der Scalp-UV ist optimal für den Zielfall 'exportierbarer, produktionstauglicher Groom', da sie die physikalische Verankerung direkt erzwingt."
                        }
                    ]
                }
            ],
            "milestone": "Du kannst SAFE-Hair im Kontext des aktuellen Forschungsfeldes einordnen, kennst verwandte Methoden und ihre Trade-offs, und kannst offene Probleme und Zukunftsrichtungen benennen."
        }
    ],
    "final_project_ideas": [
        "Führe eine vollständige Evaluation von SAFE-Hair auf einem eigenen Testset durch: Sammle 20 Porträtfotos mit verschiedenen Frisuren, Ethnien und Blickwinkeln, rekonstruiere die Haare und analysiere die Ergebnisse qualitativ und quantitativ",
        "Baue eine Mini-Pipeline, die SAFE-Hair mit Blender verbindet: Porträtfoto → SAFE-Hair → Alembic → Blender-Import → Hair-Simulation (Wind) → Rendering. Dokumentiere den gesamten Workflow",
        "Implementiere eine Vergleichsstudie: Lasse SAFE-Hair, Perm und (falls verfügbar) HairLRM auf denselben Bildern laufen und vergleiche die Ergebnisse systematisch (Metriken, visuelle Qualität, Exportierbarkeit, Geschwindigkeit)",
        "Experimentiere mit dem Conditioning: Was passiert, wenn du die DINOv2-Features modifizierst? Kannst du durch Feature-Interpolation 'Frisur-Morphing' erzeugen?"
    ],
    "further_exploration": [
        "Haarfarbe und Appearance: Erforsche Methoden, die neben Geometrie auch Haarfarbe und -textur rekonstruieren",
        "Physikbasierte Haarsimulation: Lerne die Grundlagen von Strand-Dynamics (Mass-Spring-Modelle, Discrete Elastic Rods) in Houdini oder NVIDIA Omniverse",
        "Echtzeit-Rendering von Haaren: Marschner Shading Model, Strand-based vs. Card-based Rendering in Game Engines",
        "Multi-View und Video-basierte Rekonstruktion: Methoden wie GaussianHair oder HairGS, die mehrere Bilder nutzen",
        "Generative Haarmodellierung: Text-to-Hair und Sketch-to-Hair Ansätze wie StrandDesigner"
    ],
    "glossary": [
        {
            "term": "Scalp-UV",
            "definition": "Eine 2D-Parametrisierung der Kopfhautoberfläche, die durch UV-Mapping des FLAME-Mesh entsteht. Dient als kanonischer Raum, in dem alle Haarinformationen kodiert werden."
        },
        {
            "term": "Rectified Flow",
            "definition": "Eine generative Modellierungstechnik, die Daten entlang gerader Transportpfade von einer Rauschverteilung zur Datenverteilung erzeugt. Ermöglicht schnelles Sampling in wenigen ODE-Schritten."
        },
        {
            "term": "Flow Matching",
            "definition": "Trainingsparadigma für kontinuierliche Generierungsmodelle: Man lernt ein Vektorfeld, das eine Quellverteilung (Rauschen) in eine Zielverteilung (Daten) transportiert, indem man auf bedingte Geschwindigkeiten regrediert."
        },
        {
            "term": "Persistent Follicle",
            "definition": "Ein fester Ankerpunkt auf der Scalp-UV-Map, an dem eine Haarsträhne beginnt. SAFE-Hair verwendet 32.768 solcher Follikel mit konsistenten IDs über alle Subjekte hinweg."
        },
        {
            "term": "Scalp Field",
            "definition": "Eine Multi-Channel-2D-Map über dem Scalp-UV-Raum, die pro Position Occupancy, Strangrichtungen, Längenzuweisung und Gesamtlänge kodiert."
        },
        {
            "term": "FLAME",
            "definition": "Faces Learned with an Articulated Model and Expressions – ein parametrisches 3D-Kopfmodell mit Shape-, Pose- und Expression-Parametern und fester Mesh-Topologie."
        },
        {
            "term": "DINOv2",
            "definition": "Self-Distillation with No Labels v2 – ein selbstüberwacht trainierter Vision Transformer von Meta, der universelle, semantisch reichhaltige Bildfeatures liefert."
        },
        {
            "term": "Groom",
            "definition": "In der Produktionsterminologie: Das vollständige Haarmodell eines Charakters, bestehend aus Tausenden von Strähnen mit definierten Roots, Kontrollpunkten und optional Material-Properties."
        },
        {
            "term": "Alembic (.abc)",
            "definition": "Ein offenes Austauschformat für 3D-Computergrafik, das Geometrie- und Animationsdaten speichert. Standard für den Transfer von Hair-Grooms zwischen DCC-Tools (Blender, Houdini, Maya)."
        },
        {
            "term": "Chamfer Distance",
            "definition": "Geometrische Metrik: Mittlerer nächster Nachbar-Abstand zwischen zwei Punktwolken. Bei Haarrekonstruktion: Durchschnittlicher Abstand zwischen rekonstruierten und Ground-Truth-Strangpunkten."
        },
        {
            "term": "F-Score",
            "definition": "Anteil der Punkte, die innerhalb eines Distanz-Schwellenwerts korrekt rekonstruiert sind. Misst sowohl Precision (wie nah sind rekonstruierte Punkte an GT?) als auch Recall (wie viel der GT wird abgedeckt?)."
        },
        {
            "term": "Root Validity",
            "definition": "Metrik, die den Anteil der Strähnen misst, deren Wurzelpunkt tatsächlich auf der Kopfhautoberfläche liegt. SAFE-Hair erreicht 99.8%."
        },
        {
            "term": "Occupancy",
            "definition": "Im Kontext von SAFE-Hair: Ein Skalarwert pro Follikel, der angibt, ob an dieser Position ein Haar wachsen soll (1) oder nicht (0). Steuert die Haardichte."
        },
        {
            "term": "Forward Integration",
            "definition": "Numerisches Verfahren, bei dem eine Kurve (Haarstrang) schrittweise von der Wurzel aus aufgebaut wird, indem in jedem Schritt die vorhergesagte Tangentenrichtung und Segmentlänge angewendet wird."
        },
        {
            "term": "Conditional Generation",
            "definition": "Generative Modellierung, bei der die Ausgabe durch zusätzliche Eingabeinformation (Conditioning) gesteuert wird – bei SAFE-Hair: die DINOv2-Bildfeatures steuern, welche Frisur erzeugt wird."
        },
        {
            "term": "ODE-Solver",
            "definition": "Numerisches Verfahren zur Lösung gewöhnlicher Differentialgleichungen. Bei Rectified Flow wird ein ODE-Solver verwendet, um Samples entlang des gelernten Vektorfeldes zu transportieren (z.B. Euler, RK4)."
        },
        {
            "term": "HairBench-3D",
            "definition": "Von den SAFE-Hair-Autoren eingeführter Benchmark für 3D-Haarrekonstruktion mit standardisierter Ausrichtung, Rendering und Metriken für Geometrie, Richtungskonsistenz, unsichtbare Regionen, Silhouette und Kollision."
        },
        {
            "term": "Guide Family",
            "definition": "Cluster von geometrisch ähnlichen Strähnen, die in Produktionstools als Einheit bearbeitet werden können. Ermöglicht effizientes Styling und Editing."
        }
    ]
}
```

</details>

from __future__ import annotations

import json
import queue
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from app import __version__
from app.models import (
    all_statuses,
    install_model,
    load_registry,
    registry_by_id,
    remove_model,
    status,
)
from app.paths import output_root
from app.pipeline import PipelineConfig, analyze, export_csv, export_jsonl
from app.visualization import create_figure, save_figure


BG = "#eee8dc"
PANEL = "#faf6ed"
INK = "#172126"
MUTED = "#647076"
ACCENT = "#b6482f"
TEAL = "#1f6f78"


class Workbench(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"METAPHORIQ Zero-Shot Workbench {__version__}")
        self.geometry("1320x860")
        self.minsize(1080, 720)
        self.configure(bg=BG)
        self.result: dict | None = None
        self.busy = False
        self.events: queue.Queue[tuple[str, object]] = queue.Queue()
        self.model_vars: dict[str, tk.BooleanVar] = {}
        self._configure_style()
        self._build()
        self.bind("<Control-Return>", lambda _event: self._run())
        self.after(100, self._poll_events)

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background=BG, foreground=INK, font=("Segoe UI", 10))
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background="#dcd4c6",
            foreground=INK,
            padding=(18, 10),
            font=("Segoe UI Semibold", 10),
        )
        style.map("TNotebook.Tab", background=[("selected", PANEL)])
        style.configure("Card.TFrame", background=PANEL, relief="flat")
        style.configure(
            "Accent.TButton",
            background=ACCENT,
            foreground="white",
            padding=(16, 10),
            font=("Segoe UI Semibold", 10),
        )
        style.map("Accent.TButton", background=[("active", "#923923")])
        style.configure("Treeview", rowheight=28, background="#fffdf8")
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 9))

    def _build(self) -> None:
        header = tk.Frame(self, bg=INK, height=86)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text="METAPHORIQ / ZERO-SHOT",
            bg=INK,
            fg="#f8f1e4",
            font=("Georgia", 22, "bold"),
        ).pack(side="left", padx=28)
        tk.Label(
            header,
            text="Detection · Taxonomy · Conceptual History",
            bg=INK,
            fg="#b7c7c6",
            font=("Segoe UI", 11),
        ).pack(side="left", pady=(8, 0))
        self.status_var = tk.StringVar(value="Ready. Install at least one detector.")
        tk.Label(
            header,
            textvariable=self.status_var,
            bg=INK,
            fg="#f0b77d",
            font=("Consolas", 9),
        ).pack(side="right", padx=28)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=16)
        self.work_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.models_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.plots_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.about_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.work_tab, text="Workbench")
        self.notebook.add(self.models_tab, text="Models")
        self.notebook.add(self.plots_tab, text="Scientific views")
        self.notebook.add(self.about_tab, text="Method")
        self._build_work_tab()
        self._build_models_tab()
        self._build_plots_tab()
        self._build_about_tab()

    def _build_work_tab(self) -> None:
        setup = tk.Frame(self.work_tab, bg="#e1eee9", padx=14, pady=10)
        setup.pack(fill="x", padx=14, pady=(14, 0))
        setup_copy = tk.Frame(setup, bg="#e1eee9")
        setup_copy.pack(side="left", fill="x", expand=True)
        tk.Label(
            setup_copy,
            text="0 / Make the pipeline runnable",
            bg="#e1eee9",
            fg=INK,
            font=("Segoe UI Semibold", 10),
        ).pack(anchor="w")
        self.pipeline_state_var = tk.StringVar()
        tk.Label(
            setup_copy,
            textvariable=self.pipeline_state_var,
            bg="#e1eee9",
            fg=TEAL,
            font=("Segoe UI", 9),
        ).pack(anchor="w")
        ttk.Button(
            setup,
            text="Open model library",
            command=lambda: self.notebook.select(self.models_tab),
        ).pack(side="right", padx=(8, 0))
        self.setup_button = ttk.Button(
            setup,
            text="Set up recommended pipeline",
            command=self._setup_recommended,
        )
        self.setup_button.pack(side="right")

        action_bar = tk.Frame(self.work_tab, bg=INK, padx=14, pady=10)
        action_bar.pack(side="bottom", fill="x", padx=14, pady=(0, 14))
        tk.Label(
            action_bar,
            text="Paste or open text, optionally enter its year, then run.",
            bg=INK,
            fg="#dce8e5",
            font=("Segoe UI", 10),
        ).pack(side="left")
        self.run_button = ttk.Button(
            action_bar,
            text="RUN ANALYSIS",
            style="Accent.TButton",
            command=self._run,
        )
        self.run_button.pack(side="right")

        pane = ttk.Panedwindow(self.work_tab, orient="horizontal")
        pane.pack(fill="both", expand=True, padx=14, pady=12)
        left = ttk.Frame(pane, style="Card.TFrame")
        right = ttk.Frame(pane, style="Card.TFrame")
        pane.add(left, weight=2)
        pane.add(right, weight=3)

        tk.Label(
            left,
            text="1 / Source text",
            bg=PANEL,
            fg=INK,
            font=("Georgia", 15, "bold"),
        ).pack(anchor="w")
        button_row = tk.Frame(left, bg=PANEL)
        button_row.pack(fill="x", pady=(6, 8))
        ttk.Button(button_row, text="Open text…", command=self._open_text).pack(
            side="left"
        )
        ttk.Button(button_row, text="Clear", command=self._clear).pack(
            side="left", padx=6
        )
        ttk.Button(
            button_row, text="Load runnable example", command=self._load_example
        ).pack(side="left")
        self.text = tk.Text(
            left,
            wrap="word",
            undo=True,
            bg="#fffdf8",
            fg=INK,
            insertbackground=INK,
            relief="solid",
            borderwidth=1,
            font=("Georgia", 11),
            padx=12,
            pady=12,
        )
        self.text.pack(fill="both", expand=True)

        config = tk.LabelFrame(
            left,
            text=" Pipeline configuration ",
            bg=PANEL,
            fg=INK,
            font=("Segoe UI Semibold", 10),
            padx=10,
            pady=8,
        )
        config.pack(fill="x", pady=(12, 0))
        tk.Label(config, text="Detectors", bg=PANEL, fg=MUTED).grid(
            row=0, column=0, sticky="nw", padx=(0, 12)
        )
        model_box = tk.Frame(config, bg=PANEL)
        model_box.grid(row=0, column=1, columnspan=3, sticky="w")
        for index, item in enumerate(load_registry()["models"]):
            variable = tk.BooleanVar(value=item["id"] in {"melbert", "xlmr"})
            self.model_vars[item["id"]] = variable
            tk.Checkbutton(
                model_box,
                text=item["label"] + (" · experimental" if item["experimental"] else ""),
                variable=variable,
                bg=PANEL,
                fg=INK,
                activebackground=PANEL,
                selectcolor="#fffdf8",
                command=self._refresh_pipeline_state,
            ).grid(row=index // 2, column=index % 2, sticky="w", padx=(0, 16))

        tk.Label(config, text="Ensemble", bg=PANEL, fg=MUTED).grid(
            row=2, column=0, sticky="w", pady=(9, 0)
        )
        self.ensemble_var = tk.StringVar(value="majority")
        ttk.Combobox(
            config,
            textvariable=self.ensemble_var,
            values=("majority", "union", "intersection", "average"),
            state="readonly",
            width=15,
        ).grid(row=2, column=1, sticky="w", pady=(9, 0))
        tk.Label(config, text="Threshold", bg=PANEL, fg=MUTED).grid(
            row=2, column=2, sticky="e", padx=(18, 8), pady=(9, 0)
        )
        self.threshold_var = tk.DoubleVar(value=0.5)
        ttk.Spinbox(
            config,
            from_=0.05,
            to=0.95,
            increment=0.05,
            textvariable=self.threshold_var,
            width=7,
        ).grid(row=2, column=3, sticky="w", pady=(9, 0))

        tk.Label(config, text="Taxonomy", bg=PANEL, fg=MUTED).grid(
            row=3, column=0, sticky="w", pady=(9, 0)
        )
        self.taxonomy_var = tk.StringVar(value="lexical")
        self.taxonomy_combo = ttk.Combobox(
            config,
            textvariable=self.taxonomy_var,
            values=("lexical", "xlmr", "cl_roberta"),
            state="readonly",
            width=15,
        )
        self.taxonomy_combo.grid(row=3, column=1, sticky="w", pady=(9, 0))
        tk.Label(config, text="Document year", bg=PANEL, fg=MUTED).grid(
            row=3, column=2, sticky="e", padx=(18, 8), pady=(9, 0)
        )
        self.year_var = tk.StringVar()
        ttk.Entry(config, textvariable=self.year_var, width=10).grid(
            row=3, column=3, sticky="w", pady=(9, 0)
        )
        result_header = tk.Frame(right, bg=PANEL)
        result_header.pack(fill="x")
        tk.Label(
            result_header,
            text="2 / Detected and classified spans",
            bg=PANEL,
            fg=INK,
            font=("Georgia", 15, "bold"),
        ).pack(side="left")
        ttk.Button(result_header, text="Export JSONL…", command=self._export_jsonl).pack(
            side="right"
        )
        ttk.Button(result_header, text="Export CSV…", command=self._export_csv).pack(
            side="right", padx=6
        )
        columns = (
            "word",
            "votes",
            "score",
            "family",
            "class",
            "similarity",
            "margin",
            "period",
        )
        self.results = ttk.Treeview(right, columns=columns, show="headings")
        labels = {
            "word": "Span",
            "votes": "Votes",
            "score": "Ensemble",
            "family": "Family",
            "class": "Javier class",
            "similarity": "Similarity",
            "margin": "Margin",
            "period": "Period",
        }
        widths = {
            "word": 110,
            "votes": 55,
            "score": 70,
            "family": 150,
            "class": 190,
            "similarity": 72,
            "margin": 65,
            "period": 95,
        }
        for column in columns:
            self.results.heading(column, text=labels[column])
            self.results.column(column, width=widths[column], anchor="w")
        scrollbar = ttk.Scrollbar(right, orient="vertical", command=self.results.yview)
        self.results.configure(yscrollcommand=scrollbar.set)
        self.results.pack(side="left", fill="both", expand=True, pady=(10, 0))
        scrollbar.pack(side="right", fill="y", pady=(10, 0))

    def _build_models_tab(self) -> None:
        wrapper = tk.Frame(self.models_tab, bg=PANEL)
        wrapper.pack(fill="both", expand=True, padx=18, pady=18)
        tk.Label(
            wrapper,
            text="Model library",
            bg=PANEL,
            fg=INK,
            font=("Georgia", 18, "bold"),
        ).pack(anchor="w")
        tk.Label(
            wrapper,
            text="Weights remain outside the installation. Select a row to inspect its source and license.",
            bg=PANEL,
            fg=MUTED,
        ).pack(anchor="w", pady=(2, 10))
        columns = ("label", "roles", "language", "license", "status", "size")
        self.model_tree = ttk.Treeview(wrapper, columns=columns, show="headings", height=9)
        for column, label, width in [
            ("label", "Model", 230),
            ("roles", "Roles", 160),
            ("language", "Language", 170),
            ("license", "License", 250),
            ("status", "Local status", 260),
            ("size", "Disk", 80),
        ]:
            self.model_tree.heading(column, text=label)
            self.model_tree.column(column, width=width, anchor="w")
        self.model_tree.pack(fill="x")
        self.model_tree.bind("<<TreeviewSelect>>", self._show_model_detail)
        actions = tk.Frame(wrapper, bg=PANEL)
        actions.pack(fill="x", pady=10)
        ttk.Button(
            actions, text="Download selected", command=self._download_selected
        ).pack(side="left")
        ttk.Button(actions, text="Remove selected", command=self._remove_selected).pack(
            side="left", padx=6
        )
        ttk.Button(actions, text="Refresh", command=self._refresh_models).pack(
            side="left"
        )
        ttk.Button(actions, text="Open citation", command=self._open_citation).pack(
            side="right"
        )
        self.model_detail = tk.Text(
            wrapper,
            height=13,
            wrap="word",
            bg="#fffdf8",
            fg=INK,
            relief="solid",
            borderwidth=1,
            padx=12,
            pady=10,
        )
        self.model_detail.pack(fill="both", expand=True)
        self._refresh_models()

    def _load_example(self) -> None:
        self.text.delete("1.0", "end")
        self.text.insert(
            "1.0",
            "The committee attacked the problem and planted the seeds of reform.",
        )
        self.year_var.set("1820")
        self.status_var.set("Example loaded. Select RUN ANALYSIS.")

    def _set_busy(self, busy: bool) -> None:
        self.busy = busy
        state = "disabled" if busy else "normal"
        self.run_button.configure(state=state)
        self.setup_button.configure(state=state)

    def _refresh_pipeline_state(self) -> None:
        ready = [item.model_id for item in all_statuses() if item.ready]
        selected = self._selected_models()
        if selected and all(model_id in ready for model_id in selected):
            message = (
                f"Ready to run: {len(selected)} selected detector"
                f"{'s' if len(selected) != 1 else ''}."
            )
        elif ready:
            message = (
                f"{len(ready)} detector{'s' if len(ready) != 1 else ''} installed; "
                "some selected detectors still need downloading."
            )
        else:
            message = "No detector installed. Use the setup button, or Run to download."
        self.pipeline_state_var.set(message)

    def _setup_recommended(self) -> None:
        recommended = tuple(
            item["id"] for item in load_registry()["models"] if item["recommended"]
        )
        for model_id, variable in self.model_vars.items():
            variable.set(model_id in recommended)
        missing = [model_id for model_id in recommended if not status(model_id).ready]
        self._refresh_pipeline_state()
        if not missing:
            self.status_var.set("Recommended pipeline is ready.")
            return
        labels = "\n".join(f"- {registry_by_id()[item]['label']}" for item in missing)
        if not messagebox.askyesno(
            "Set up recommended pipeline",
            "Download the recommended detectors?\n\n"
            f"{labels}\n\n"
            "The combined download is approximately 1.6 GB.",
        ):
            return
        self._set_busy(True)

        def task() -> None:
            try:
                for model_id in missing:
                    install_model(
                        model_id,
                        progress=lambda message: self.events.put(("status", message)),
                    )
                self.events.put(("models", "Recommended pipeline ready"))
            except Exception as error:
                self.events.put(("error", str(error)))

        threading.Thread(target=task, daemon=True).start()

    def _build_plots_tab(self) -> None:
        toolbar = tk.Frame(self.plots_tab, bg=PANEL)
        toolbar.pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(
            toolbar,
            text="Scientific views",
            bg=PANEL,
            fg=INK,
            font=("Georgia", 18, "bold"),
        ).pack(side="left")
        ttk.Button(toolbar, text="Save PNG…", command=self._save_plot).pack(
            side="right"
        )
        self.plot_host = tk.Frame(self.plots_tab, bg=PANEL)
        self.plot_host.pack(fill="both", expand=True, padx=12, pady=8)
        self._render_plot()

    def _build_about_tab(self) -> None:
        text = tk.Text(
            self.about_tab,
            wrap="word",
            bg=PANEL,
            fg=INK,
            relief="flat",
            padx=34,
            pady=26,
            font=("Georgia", 11),
        )
        text.pack(fill="both", expand=True)
        text.insert(
            "1.0",
            """Method and limits

This program separates three claims:

DETECTION asks whether a word is used metaphorically. MelBERT, XLM-R, CreativeLang RoBERTa, and FrameBERT operate here.

CLASSIFICATION asks which Javier taxonomy class best resembles the detected context. The built-in method compares the context with accepted annotated samples. XLM-R and CreativeLang encoders are optional prototype spaces. These predictions require review.

CHRONOLOGY assigns a period from an explicit document year. It does not infer dates from prose. The 1946–1949 interval is retained as a transition gap because the requested chronology stops at 1945 and resumes in 1950.

Counts describe the analyzed input. They are not historical prevalence estimates. Model agreement, similarity, and margin are diagnostics, not calibrated certainty.
""",
        )
        text.configure(state="disabled")

    def _open_text(self) -> None:
        name = filedialog.askopenfilename(
            filetypes=[("Text", "*.txt"), ("JSON Lines", "*.jsonl"), ("All files", "*.*")]
        )
        if not name:
            return
        path = Path(name)
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(encoding="cp1252")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)

    def _clear(self) -> None:
        self.text.delete("1.0", "end")
        self.result = None
        self._fill_results()
        self._render_plot()

    def _selected_models(self) -> tuple[str, ...]:
        return tuple(
            model_id for model_id, variable in self.model_vars.items() if variable.get()
        )

    def _run(self) -> None:
        if self.busy:
            return
        text = self.text.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo(
                "Add source text",
                "Paste text, open a text file, or select Load runnable example.",
            )
            return
        models = self._selected_models()
        if not models:
            messagebox.showinfo(
                "Select a detector",
                "Select at least one detector, or use Set up recommended pipeline.",
            )
            return
        missing = [model_id for model_id in models if not status(model_id).ready]
        if missing:
            labels = "\n".join(f"- {registry_by_id()[item]['label']}" for item in missing)
            if not messagebox.askyesno(
                "Download and run",
                "These selected detectors must be downloaded first:\n\n"
                f"{labels}\n\nDownload them now and continue automatically?",
            ):
                return
        taxonomy_method = self.taxonomy_var.get()
        if (
            taxonomy_method != "lexical"
            and not status(taxonomy_method).ready
            and taxonomy_method not in missing
        ):
            if not messagebox.askyesno(
                "Download taxonomy encoder",
                f"{registry_by_id()[taxonomy_method]['label']} is required for "
                "the selected taxonomy method.\n\nDownload it and continue?",
            ):
                return
            missing.append(taxonomy_method)
        try:
            year = int(self.year_var.get()) if self.year_var.get().strip() else None
        except ValueError:
            messagebox.showerror("Invalid year", "Document year must be an integer.")
            return
        config = PipelineConfig(
            model_ids=models,
            ensemble_rule=self.ensemble_var.get(),
            detection_threshold=float(self.threshold_var.get()),
            taxonomy_method=taxonomy_method,
            document_year=year,
        )
        self._set_busy(True)
        self.status_var.set("Running…")

        def task() -> None:
            try:
                for model_id in missing:
                    install_model(
                        model_id,
                        progress=lambda message: self.events.put(("status", message)),
                    )
                result = analyze(
                    text,
                    config,
                    progress=lambda message: self.events.put(("status", message)),
                )
                self.events.put(("analysis", result))
            except Exception as error:
                self.events.put(("error", str(error)))

        threading.Thread(target=task, daemon=True).start()

    def _poll_events(self) -> None:
        try:
            while True:
                event, payload = self.events.get_nowait()
                if event == "status":
                    self.status_var.set(str(payload))
                elif event == "analysis":
                    self.result = payload  # type: ignore[assignment]
                    self.status_var.set(
                        f"Complete · {len(self.result['detections'])} detected spans"
                    )
                    self._set_busy(False)
                    self._refresh_models()
                    self._fill_results()
                    self._render_plot()
                elif event == "models":
                    self.status_var.set(str(payload))
                    self._set_busy(False)
                    self._refresh_models()
                elif event == "error":
                    self.status_var.set("Operation failed")
                    self._set_busy(False)
                    messagebox.showerror("METAPHORIQ", str(payload))
        except queue.Empty:
            pass
        self.after(100, self._poll_events)

    def _fill_results(self) -> None:
        for item in self.results.get_children():
            self.results.delete(item)
        if not self.result:
            return
        for row in self.result["detections"]:
            taxonomy = row["taxonomy"]
            self.results.insert(
                "",
                "end",
                values=(
                    row["word"],
                    f"{row['positive_votes']}/{row['model_count']}",
                    f"{row['ensemble_score']:.3f}",
                    f"{taxonomy['family_id']} {taxonomy['family_label']}",
                    f"{taxonomy['class_id']} {taxonomy['class_label']}",
                    f"{taxonomy['similarity']:.3f}",
                    f"{taxonomy['margin']:.3f}",
                    row["period"]["id"],
                ),
            )

    def _export_jsonl(self) -> None:
        if not self.result:
            return
        name = filedialog.asksaveasfilename(
            initialdir=output_root(),
            defaultextension=".jsonl",
            filetypes=[("JSON Lines", "*.jsonl")],
        )
        if name:
            export_jsonl(self.result, Path(name))

    def _export_csv(self) -> None:
        if not self.result:
            return
        name = filedialog.asksaveasfilename(
            initialdir=output_root(),
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
        )
        if name:
            export_csv(self.result, Path(name))

    def _refresh_models(self) -> None:
        previous = self._selected_model_id()
        for item in self.model_tree.get_children():
            self.model_tree.delete(item)
        statuses = {item.model_id: item for item in all_statuses()}
        for spec in load_registry()["models"]:
            current = statuses[spec["id"]]
            self.model_tree.insert(
                "",
                "end",
                iid=spec["id"],
                values=(
                    spec["label"],
                    ", ".join(spec["role"]),
                    ", ".join(spec["languages"]),
                    spec["license"],
                    current.detail,
                    f"{current.bytes / 1024**2:.0f} MB" if current.bytes else "—",
                ),
            )
        children = self.model_tree.get_children()
        if children:
            target = previous if previous in children else next(
                (
                    item["id"]
                    for item in load_registry()["models"]
                    if not statuses[item["id"]].ready
                ),
                children[0],
            )
            self.model_tree.selection_set(target)
            self.model_tree.focus(target)
            self._show_model_detail()
        self._refresh_pipeline_state()

    def _selected_model_id(self) -> str | None:
        selection = self.model_tree.selection()
        return selection[0] if selection else None

    def _show_model_detail(self, _event=None) -> None:
        model_id = self._selected_model_id()
        if not model_id:
            return
        spec = registry_by_id()[model_id]
        current = status(model_id)
        detail = {
            "id": model_id,
            "status": current.detail,
            "local_path": str(current.path),
            "source": spec.get("repository_id") or spec.get("repository"),
            "license": spec["license"],
            "training_data": spec["training_data"],
            "citation": spec["citation_url"],
            "notes": spec["notes"],
        }
        self.model_detail.configure(state="normal")
        self.model_detail.delete("1.0", "end")
        self.model_detail.insert("1.0", json.dumps(detail, indent=2, ensure_ascii=False))
        self.model_detail.configure(state="disabled")

    def _download_selected(self) -> None:
        model_id = self._selected_model_id()
        if not model_id:
            messagebox.showinfo("Select a model", "Select a model row to download.")
            return
        spec = registry_by_id()[model_id]
        if not messagebox.askyesno(
            "Download model",
            f"Download {spec['label']} from its upstream source?\n\n"
            f"License: {spec['license']}\n\n"
            "The download may be several hundred megabytes.",
        ):
            return
        self._set_busy(True)

        def task() -> None:
            try:
                install_model(
                    model_id,
                    progress=lambda message: self.events.put(("status", message)),
                )
                self.events.put(("models", f"{spec['label']} ready"))
            except Exception as error:
                self.events.put(("error", str(error)))

        threading.Thread(target=task, daemon=True).start()

    def _remove_selected(self) -> None:
        model_id = self._selected_model_id()
        if not model_id:
            return
        spec = registry_by_id()[model_id]
        if messagebox.askyesno("Remove model", f"Remove local files for {spec['label']}?"):
            remove_model(model_id)
            self._refresh_models()

    def _open_citation(self) -> None:
        model_id = self._selected_model_id()
        if model_id:
            webbrowser.open(registry_by_id()[model_id]["citation_url"])

    def _render_plot(self) -> None:
        for child in self.plot_host.winfo_children():
            child.destroy()
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        figure = create_figure(self.result or {"detections": []})
        canvas = FigureCanvasTkAgg(figure, master=self.plot_host)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.plot_canvas = canvas

    def _save_plot(self) -> None:
        if not self.result:
            return
        name = filedialog.asksaveasfilename(
            initialdir=output_root(),
            defaultextension=".png",
            filetypes=[("PNG image", "*.png")],
        )
        if name:
            save_figure(self.result, Path(name))


def run() -> None:
    Workbench().mainloop()

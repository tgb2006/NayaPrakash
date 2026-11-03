"""Registry and deduplication manager for examples and chapter progress."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
from src.models.naya import ExampleItem

class RegistryManager:
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent.parent
        self.data_dir = self.base_dir / "data"
        self.examples_file = self.data_dir / "examples_registry.json"
        self.progress_file = self.data_dir / "progress_tracker.json"
        self._examples_data: Optional[Dict[str, Any]] = None
        self._progress_data: Optional[Dict[str, Any]] = None

    def load_examples(self) -> Dict[str, Any]:
        if not self.examples_file.exists():
            self._examples_data = {"total_examples": 0, "examples": []}
            self.save_examples()
        else:
            with open(self.examples_file, "r", encoding="utf-8") as f:
                self._examples_data = json.load(f)
        return self._examples_data

    def save_examples(self) -> None:
        if self._examples_data is not None:
            with open(self.examples_file, "w", encoding="utf-8") as f:
                json.dump(self._examples_data, f, ensure_ascii=False, indent=2)

    def get_all_examples(self) -> List[ExampleItem]:
        data = self.load_examples()
        return [ExampleItem(**item) for item in data.get("examples", [])]

    def add_examples_for_chapter(self, chapter_id: Union[int, float, str], naya_name: str, examples: List[Dict[str, Any]]) -> None:
        data = self.load_examples()
        current_examples = data.get("examples", [])
        
        # Remove any existing examples for this chapter if re-drafting
        current_examples = [e for e in current_examples if str(e.get("chapter_id")) != str(chapter_id)]

        start_id = len(current_examples) + 1
        for idx, ex in enumerate(examples, start=1):
            ex_item = {
                "id": start_id + idx - 1,
                "chapter_id": chapter_id,
                "naya_name": naya_name,
                "example_number": idx,
                "title": ex.get("title", f"उदाहरण {idx}"),
                "theme": ex.get("theme", "सामान्य"),
                "core_incident_summary": ex.get("summary", ""),
                "keywords": ex.get("keywords", [])
            }
            current_examples.append(ex_item)

        data["examples"] = current_examples
        data["total_examples"] = len(current_examples)
        self._examples_data = data
        self.save_examples()

    def check_duplicate(self, title: str, summary: str, keywords: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Checks if a story or title is too similar to any previously recorded story."""
        data = self.load_examples()
        existing = data.get("examples", [])
        matches = []
        
        title_lower = title.strip().lower()
        summary_words = set(summary.lower().split())
        kw_set = set(k.lower() for k in (keywords or []))

        for ex in existing:
            ex_title = ex.get("title", "").strip().lower()
            ex_summary_words = set(ex.get("core_incident_summary", "").lower().split())
            ex_kw_set = set(k.lower() for k in ex.get("keywords", []))

            # Exact or partial title match
            if title_lower and (title_lower == ex_title or title_lower in ex_title or ex_title in title_lower):
                matches.append({"reason": "Title overlap", "matched_example": ex})
                continue

            # Heavy keyword overlap
            if kw_set and ex_kw_set:
                overlap = kw_set.intersection(ex_kw_set)
                if len(overlap) >= 3:
                    matches.append({"reason": f"Shared keywords: {list(overlap)}", "matched_example": ex})
                    continue

        return matches

    def get_used_themes_context(self, max_recent: int = 50) -> str:
        """Returns a formatted list of recent story titles and themes to avoid in prompts."""
        examples = self.get_all_examples()
        if not examples:
            return "अभी तक कोई उदाहरण पूर्व अध्यायों में दर्ज नहीं है।"

        recent = examples[-max_recent:]
        lines = []
        for e in recent:
            lines.append(f"- [अध्याय {e.chapter_id}: {e.naya_name}] शीर्षक: '{e.title}' | विषय: {e.theme}")
        return "\n".join(lines)

    def load_progress(self) -> Dict[str, Any]:
        if not self.progress_file.exists():
            return {}
        with open(self.progress_file, "r", encoding="utf-8") as f:
            self._progress_data = json.load(f)
        return self._progress_data

    def save_progress(self) -> None:
        if self._progress_data is not None:
            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump(self._progress_data, f, ensure_ascii=False, indent=2)

    def update_chapter_status(
        self,
        chapter_id: Union[int, float, str],
        status: str,
        file_path: Optional[str] = None,
        word_count: int = 0,
        is_valid: bool = False
    ) -> None:
        data = self.load_progress()
        ch_key = str(chapter_id)
        if "chapters_state" in data and ch_key in data["chapters_state"]:
            old_status = data["chapters_state"][ch_key].get("status")
            khanda_id = str(data["chapters_state"][ch_key].get("khanda_id", 1))

            data["chapters_state"][ch_key].update({
                "status": status,
                "file_path": file_path,
                "word_count": word_count,
                "validation_passed": is_valid
            })

            # Update completed counts
            if old_status != "completed" and status == "completed":
                data["completed_count"] = data.get("completed_count", 0) + 1
                data["pending_count"] = max(0, data.get("pending_count", 0) - 1)
                if khanda_id in data.get("khanda_progress", {}):
                    data["khanda_progress"][khanda_id]["completed"] += 1

            self._progress_data = data
            self.save_progress()

    def get_dashboard_summary(self) -> Dict[str, Any]:
        data = self.load_progress()
        total_nayas = data.get("total_nayas", 203)
        completed = data.get("completed_count", 0)
        pending = data.get("pending_count", total_nayas)
        percent = (completed / total_nayas) * 100 if total_nayas > 0 else 0

        examples_data = self.load_examples()
        total_examples = examples_data.get("total_examples", 0)

        return {
            "total_nayas": total_nayas,
            "completed": completed,
            "pending": pending,
            "percent_completed": round(percent, 2),
            "total_unique_examples": total_examples,
            "khanda_progress": data.get("khanda_progress", {})
        }

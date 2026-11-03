"""Catalog loader for Naya Prakash Book."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
import yaml

from src.models.naya import NayaCatalogItem, KhandaDefinition

class CatalogLoader:
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent.parent
        self.config_dir = self.base_dir / "config"
        self._book_config: Optional[Dict[str, Any]] = None
        self._khandas: Optional[List[KhandaDefinition]] = None
        self._nayas: Optional[List[NayaCatalogItem]] = None

    def get_book_config(self) -> Dict[str, Any]:
        if self._book_config is None:
            path = self.config_dir / "book_config.yaml"
            with open(path, "r", encoding="utf-8") as f:
                self._book_config = yaml.safe_load(f)
        return self._book_config

    def get_khandas(self) -> List[KhandaDefinition]:
        if self._khandas is None:
            path = self.config_dir / "khanda_definitions.yaml"
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            self._khandas = [KhandaDefinition(**item) for item in data.get("khandas", [])]
        return self._khandas

    def get_khanda_by_id(self, khanda_id: int) -> Optional[KhandaDefinition]:
        for k in self.get_khandas():
            if k.id == khanda_id:
                return k
        return None

    def get_all_nayas(self) -> List[NayaCatalogItem]:
        if self._nayas is None:
            path = self.config_dir / "nayas_master_catalog.json"
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._nayas = [NayaCatalogItem(**item) for item in data.get("nayas", [])]
        return self._nayas

    def get_naya_by_id(self, naya_id: Union[int, float, str]) -> Optional[NayaCatalogItem]:
        target = str(naya_id)
        for n in self.get_all_nayas():
            if str(n.id) == target:
                return n
        return None

    def get_nayas_by_khanda(self, khanda_id: int) -> List[NayaCatalogItem]:
        return [n for n in self.get_all_nayas() if n.khanda_id == khanda_id]

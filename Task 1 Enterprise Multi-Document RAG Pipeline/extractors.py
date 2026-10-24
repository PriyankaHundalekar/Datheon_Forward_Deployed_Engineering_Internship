import os
import pandas as pd
from pypdf import PdfReader

class DocumentExtractor:
    """Extracts raw text and base metadata from multi-format enterprise files."""
    
    @staticmethod
    def extract_pdf(file_path: str, department: str, access_tier: str) -> list[dict]:
        reader = PdfReader(file_path)
        documents = []
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                documents.append({
                    "content": text.strip(),
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "page": page_num + 1,
                        "department": department,
                        "access_tier": access_tier,
                        "file_type": "pdf"
                    }
                })
        return documents

    @staticmethod
    def extract_csv(file_path: str, department: str, access_tier: str) -> list[dict]:
        df = pd.read_csv(file_path)
        documents = []
        for index, row in df.iterrows():
            # Convert row to a clean readable string format for embedding
            row_text = ", ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
            documents.append({
                "content": row_text,
                "metadata": {
                    "source": os.path.basename(file_path),
                    "row_index": index,
                    "department": department,
                    "access_tier": access_tier,
                    "file_type": "csv"
                }
            })
        return documents

    @staticmethod
    def extract_markdown(file_path: str, department: str, access_tier: str) -> list[dict]:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return [{
            "content": text.strip(),
            "metadata": {
                "source": os.path.basename(file_path),
                "department": department,
                "access_tier": access_tier,
                "file_type": "markdown"
            }
        }]
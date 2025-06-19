import os
import sys

import django

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.models import Document


def main():
    document_count = Document.objects.count()
    print(f"document count: {document_count}")


if __name__ == '__main__':
    main()

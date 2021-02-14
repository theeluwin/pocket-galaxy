import os
import sys
import django

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.models import (
    Document,
)


def main():
    document_count = Document.objects.count()
    print(f"document count: {document_count}")


if __name__ == '__main__':
    main()

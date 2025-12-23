#!/usr/bin/env python3
"""
AI Math Mentor - System Diagnostic Tool
Run this to identify all system issues at once
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

def print_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def check_environment():
    """Check environment setup"""
    print_header("1. ENVIRONMENT CHECK")
    
    # Python version
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check .env file
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        print("✓ .env file found")
        load_dotenv(env_path)
        
        # Check for required keys
        keys_to_check = {
            'GEMINI_API_KEY': 'Required for AI functionality',
            'GEMINI_MODEL': 'Optional (defaults to gemini-1.5-flash)'
        }
        
        for key, description in keys_to_check.items():
            value = os.getenv(key)
            if value:
                # Don't print full key for security
                masked = value[:8] + "..." if len(value) > 8 else "***"
                print(f"✓ {key}: {masked} ({description})")
            else:
                print(f"✗ {key}: NOT SET - {description}")
    else:
        print(f"✗ .env file not found at {env_path}")
        print("  → Create .env from .env.example and add your API keys")

def check_dependencies():
    """Check if all packages are installed"""
    print_header("2. DEPENDENCIES CHECK")
    
    required = {
        'streamlit': 'Web UI framework',
        'google-generativeai': 'Gemini API client',
        'langchain': 'LLM framework',
        'langchain_community': 'LangChain community integrations',
        'sentence_transformers': 'Embeddings for RAG',
        'faiss': 'Vector database (faiss-cpu)',
        'easyocr': 'OCR for image input',
        'chromadb': 'Alternative vector store',
        'pillow': 'Image processing',
        'numpy': 'Numerical computing',
        'pydantic': 'Data validation'
    }
    
    missing = []
    for package, description in required.items():
        try:
            pkg_name = package.replace('-', '_')
            if pkg_name == 'google_generativeai':
                pkg_name = 'google.generativeai'
            __import__(pkg_name)
            print(f"✓ {package:<30} - {description}")
        except ImportError:
            print(f"✗ {package:<30} - {description}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print(f"  → Run: pip install {' '.join(missing)}")

def check_project_structure():
    """Check if required directories and files exist"""
    print_header("3. PROJECT STRUCTURE CHECK")
    
    base_path = Path(__file__).parent.parent
    
    required_paths = {
        'backend': 'Main backend code',
        'backend/agents': 'Agent implementations',
        'backend/utils': 'Utility modules',
        'backend/rag': 'RAG pipeline',
        'backend/memory': 'Memory system',
        'backend/knowledge_base': 'Knowledge base files',
        'backend/app.py': 'Streamlit application',
        'backend/validate.py': 'Validation script',
        '.env.example': 'Environment template'
    }
    
    for path, description in required_paths.items():
        full_path = base_path / path
        if full_path.exists():
            print(f"✓ {path:<35} - {description}")
        else:
            print(f"✗ {path:<35} - {description} (MISSING)")

def check_knowledge_base():
    """Check knowledge base files"""
    print_header("4. KNOWLEDGE BASE CHECK")
    
    kb_path = Path(__file__).parent.parent / 'backend' / 'knowledge_base'
    
    if not kb_path.exists():
        print(f"✗ Knowledge base directory not found at {kb_path}")
        return
    
    kb_files = list(kb_path.glob('*.md'))
    
    if kb_files:
        print(f"✓ Found {len(kb_files)} knowledge base files:")
        for kb_file in kb_files:
            size_kb = kb_file.stat().st_size / 1024
            print(f"  - {kb_file.name:<35} ({size_kb:.1f} KB)")
    else:
        print("✗ No .md files found in knowledge_base/")

def test_api_connections():
    """Test if APIs work"""
    print_header("5. API CONNECTION TEST")
    
    # Test Gemini
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("✗ Gemini API: No API key found")
            return
        
        genai.configure(api_key=api_key)  # type: ignore[attr-defined]
        
        model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
        print(f"  Testing with model: {model_name}")
        
        model = genai.GenerativeModel(model_name)  # type: ignore[attr-defined]
        response = model.generate_content("Respond with just the word 'working' if you can see this.")
        
        result_text = response.text[:50]
        print(f"✓ Gemini API: Connected successfully")
        print(f"  Response preview: {result_text}")
        
    except Exception as e:
        print(f"✗ Gemini API: Failed")
        print(f"  Error: {str(e)[:200]}")
        print("  → Check your GEMINI_API_KEY in .env")
        print("  → Verify API key is valid at https://makersuite.google.com/app/apikey")

def test_imports():
    """Test importing main modules"""
    print_header("6. MODULE IMPORT TEST")
    
    modules_to_test = [
        ('utils.config', 'Configuration loader'),
        ('utils.logger', 'Logging setup'),
        ('agents.base_agent', 'Base agent class'),
        ('utils.orchestrator', 'Main orchestrator'),
    ]
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✓ {module_name:<30} - {description}")
        except Exception as e:
            print(f"✗ {module_name:<30} - {description}")
            print(f"  Error: {str(e)[:100]}")

def check_vector_store():
    """Check if vector store exists"""
    print_header("7. VECTOR STORE CHECK")
    
    vector_store_path = Path(__file__).parent.parent / 'backend' / 'vector_store'
    
    if vector_store_path.exists():
        files = list(vector_store_path.glob('*'))
        if files:
            print(f"✓ Vector store directory exists with {len(files)} files")
            for f in files:
                print(f"  - {f.name}")
        else:
            print("⚠ Vector store directory exists but is empty")
            print("  → Vector store will be created on first run")
    else:
        print("⚠ Vector store directory not found")
        print("  → Will be created automatically on first run")

def generate_summary():
    """Generate summary and recommendations"""
    print_header("SUMMARY & RECOMMENDATIONS")
    
    print("\n✓ = Working correctly")
    print("⚠ = Warning (may work but needs attention)")
    print("✗ = Error (needs to be fixed)")
    
    print("\n📝 Next Steps:")
    print("1. Fix any ✗ errors shown above")
    print("2. Review ⚠ warnings and address if needed")
    print("3. Run: cd backend && python3 validate.py")
    print("4. Run: cd backend && streamlit run app.py")
    
    print("\n💡 Common Issues:")
    print("- Missing GEMINI_API_KEY: Add to .env file")
    print("- Missing packages: Run pip install -r requirements.txt")
    print("- Import errors: Check Python path and module structure")
    print("- API errors: Verify API key is valid and has quota")

def main():
    """Run all diagnostic checks"""
    print("\n" + "🔍 " * 20)
    print("  AI MATH MENTOR - SYSTEM DIAGNOSTIC TOOL")
    print("🔍 " * 20)
    
    try:
        check_environment()
        check_dependencies()
        check_project_structure()
        check_knowledge_base()
        test_api_connections()
        test_imports()
        check_vector_store()
        generate_summary()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Diagnostic interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n✗ Diagnostic failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 60)
    print("  DIAGNOSTIC COMPLETE")
    print("=" * 60 + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

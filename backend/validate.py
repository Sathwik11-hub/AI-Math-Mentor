"""
Quick validation script to test imports and basic functionality
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from utils.config import Config
        print("✓ Config imported")
        
        from utils.logger import setup_logger
        print("✓ Logger imported")
        
        from utils.input_handlers import ImageInputHandler, AudioInputHandler, TextInputHandler
        print("✓ Input handlers imported")
        
        from agents.base_agent import BaseAgent
        print("✓ Base agent imported")
        
        from agents.parser_agent import ParserAgent
        print("✓ Parser agent imported")
        
        from agents.intent_router_agent import IntentRouterAgent
        print("✓ Intent router agent imported")
        
        from agents.solver_agent import SolverAgent
        print("✓ Solver agent imported")
        
        from agents.verifier_agent import VerifierAgent
        print("✓ Verifier agent imported")
        
        from agents.explainer_agent import ExplainerAgent
        print("✓ Explainer agent imported")
        
        from rag.rag_pipeline import RAGPipeline
        print("✓ RAG pipeline imported")
        
        from memory.memory_system import MemorySystem
        print("✓ Memory system imported")
        
        from utils.orchestrator import MathMentorOrchestrator
        print("✓ Orchestrator imported")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_basic_functionality():
    """Test basic functionality without API calls"""
    print("\nTesting basic functionality...")
    
    try:
        from utils.config import Config
        from utils.logger import setup_logger
        from memory.memory_system import MemorySystem
        
        # Test logger
        logger = setup_logger("test")
        logger.info("Logger test")
        print("✓ Logger works")
        
        # Test config (without validation since we don't have API key)
        print(f"✓ Config loaded, supported topics: {Config.SUPPORTED_TOPICS}")
        
        # Test memory system
        memory = MemorySystem()
        print("✓ Memory system initialized")
        
        print("\n✅ Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_knowledge_base():
    """Check knowledge base files"""
    print("\nChecking knowledge base...")
    
    from pathlib import Path
    kb_dir = Path("knowledge_base")
    
    if not kb_dir.exists():
        print("❌ Knowledge base directory not found")
        return False
    
    expected_files = [
        "algebra_formulas.md",
        "calculus_concepts.md",
        "probability_concepts.md",
        "linear_algebra_basics.md",
        "common_mistakes.md",
        "solution_templates.md"
    ]
    
    all_found = True
    for file in expected_files:
        file_path = kb_dir / file
        if file_path.exists():
            print(f"✓ {file}")
        else:
            print(f"❌ {file} not found")
            all_found = False
    
    if all_found:
        print("\n✅ All knowledge base files present!")
    
    return all_found


if __name__ == "__main__":
    print("=" * 60)
    print("AI Math Mentor - Validation Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Basic Functionality", test_basic_functionality()))
    results.append(("Knowledge Base", check_knowledge_base()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All validation tests passed!")
        print("\nNext steps:")
        print("1. Set GEMINI_API_KEY in .env file")
        print("2. Run: streamlit run app.py")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)

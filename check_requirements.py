"""Check if all requirements are met for the LLM Customer Support Agent"""
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError:
        print(f"❌ {package_name} (not installed)")
        return False

def check_directories():
    """Check if required directories exist"""
    required_dirs = [
        "data/documents",
        "data/faiss_index",
        "data/vector_db"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ Directory: {dir_path}")
        else:
            print(f"⚠️  Directory missing: {dir_path} (will be created)")
            path.mkdir(parents=True, exist_ok=True)
            all_exist = False
    
    return all_exist

def check_files():
    """Check if required files exist"""
    required_files = [
        ".env",
        "requirements.txt",
        "src/config.py",
        "api/main.py",
        "streamlit_app.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ File: {file_path}")
        else:
            print(f"❌ File missing: {file_path}")
            all_exist = False
    
    return all_exist

def check_gpu():
    """Check if GPU is available"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
            return True
        else:
            print("⚠️  GPU not available (CPU mode will be used)")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed, cannot check GPU")
        return False

def main():
    """Main check function"""
    print("🔍 Checking requirements for LLM Customer Support Agent...\n")
    
    checks = []
    
    print("Python Version:")
    checks.append(check_python_version())
    print()
    
    print("Required Packages:")
    packages = [
        ("langchain", "langchain"),
        ("transformers", "transformers"),
        ("sentence-transformers", "sentence_transformers"),
        ("faiss-cpu", "faiss"),
        ("mlflow", "mlflow"),
        ("fastapi", "fastapi"),
        ("streamlit", "streamlit"),
        ("pydantic", "pydantic"),
        ("pypdf", "pypdf"),
    ]
    
    for package, import_name in packages:
        checks.append(check_package(package, import_name))
    print()
    
    print("Directories:")
    checks.append(check_directories())
    print()
    
    print("Files:")
    checks.append(check_files())
    print()
    
    print("Hardware:")
    check_gpu()
    print()
    
    if all(checks):
        print("✅ All requirements met! You're ready to go.")
        return 0
    else:
        print("❌ Some requirements are missing. Please install them:")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())


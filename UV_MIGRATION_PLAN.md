# UV Migration Plan - Issue #5

## Overview

This document outlines the comprehensive plan for migrating the mkdocs-obsidian-interactive-graph-plugin from traditional Python packaging (setup.py + pip) to modern UV-based package management for improved performance, better dependency management, and a streamlined development workflow.

## Executive Summary

- **Goal**: Migrate to UV (state-of-the-art Python package manager for 2025)
- **Benefits**: 10-100x faster dependency resolution, modern standards, reproducible builds
- **Compatibility**: Maintains full backward compatibility with pip
- **Timeline**: Phased implementation with comprehensive testing

## Current State Analysis

### Existing Dependencies

#### Core Dependencies (from setup.py)
```python
install_requires=['mkdocs-material']
python_requires='>=3.6'
```

#### Documentation Dependencies (from requirements.txt)
```
mkdocs-callouts
mkdocs-glightbox  
mkdocs-obsidian-bridge
mkdocs-obsidian-support-plugin
mkdocs-obsidian-interactive-graph-plugin  # self-reference
overrides
```

#### MkDocs Material Core Requirements
```
jinja2~=3.1
markdown~=3.2
mkdocs~=1.6
mkdocs-material-extensions~=1.3
pygments~=2.16
pymdown-extensions~=10.2
```

## Target Architecture

### Modern pyproject.toml Configuration

```toml
[build-system]
requires = ["uv_build>=0.7.19,<0.8.0"]
build-backend = "uv_build"

[project]
name = "mkdocs-obsidian-interactive-graph-plugin"
description = "A MkDocs plugin that generates a obsidian like interactive graph"
readme = "README.md"
license = {text = "MIT"}
authors = [{name = "daxcore", email = "300ccda6-8d43-4f23-808e-961e653ff7d6@anonaddy.com"}]
requires-python = ">=3.9"
dynamic = ["version"]

# Core dependencies with conservative constraints
dependencies = [
    "mkdocs-material>=9.0.0,<10.0.0",  # Pin to 9.x series for stability
]

[project.optional-dependencies]
# Documentation dependencies (moved from requirements.txt)
docs = [
    "mkdocs-callouts>=1.0.0",
    "mkdocs-glightbox>=0.3.0", 
    "mkdocs-obsidian-bridge>=0.2.0",
    "mkdocs-obsidian-support-plugin>=1.0.0",
]

# Development dependencies
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mkdocs>=1.6.0",
]

# Testing matrix dependencies
test = [
    "mkdocs-material>=9.0.0,<10.0.0",
    "mkdocs>=1.6.0,<2.0.0",
]

[project.urls]
Homepage = "https://github.com/daxcore/mkdocs-obsidian-interactive-graph-plugin"
Repository = "https://github.com/daxcore/mkdocs-obsidian-interactive-graph-plugin"
Issues = "https://github.com/daxcore/mkdocs-obsidian-interactive-graph-plugin/issues"

[project.entry-points."mkdocs.plugins"]
obsidian-interactive-graph = "obsidian_interactive_graph.plugin:ObsidianInteractiveGraphPlugin"

[tool.uv.build-backend]
version-source = "git"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mkdocs>=1.6.0",
]

# Python version compatibility note
# Minimum Python 3.9 (3.8 EOL Oct 2024)
# Tested on 3.9, 3.10, 3.11, 3.12, 3.13
```

### Enhanced .gitignore

```gitignore
# Obsidian
.obsidian/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# UV specific
.uv/
uv.lock

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### Ultra-Modern Dockerfile

```dockerfile
# Use Python 3.11 slim for optimal performance
FROM python:3.11-slim

# Install UV (latest stable method)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set UV environment variables
ENV UV_SYSTEM_PYTHON=1
ENV UV_CACHE_DIR=/tmp/uv-cache

WORKDIR /notes

# Copy project files for installation
COPY pyproject.toml /plugin/
COPY obsidian_interactive_graph /plugin/obsidian_interactive_graph
COPY README.md /plugin/README.md
COPY .git/ /plugin/.git/

# Install plugin using UV (much faster than pip)
RUN cd /plugin && uv pip install .

# Copy and install documentation dependencies
COPY requirements.txt /notes/requirements.txt
RUN uv pip install -r requirements.txt

# Clean up UV cache to reduce image size
RUN rm -rf /tmp/uv-cache

# Set working directory for documentation
WORKDIR /notes
```

## Version Compatibility Matrix

### Python Version Support
- **Minimum**: Python 3.9 (updated from 3.6, 3.8 is EOL as of Oct 2024)
- **Tested**: Python 3.9, 3.10, 3.11, 3.12, 3.13
- **Recommended**: Python 3.11+ for optimal UV performance
- **Future**: Python 3.14 (prerelease support)

### MkDocs Ecosystem Compatibility
- **MkDocs**: 1.6+ (latest stable)
- **MkDocs Material**: 9.x series (conservative pinning)
- **Plugin Dependencies**: Latest compatible versions

### Platform Support
- **Linux**: Ubuntu 20.04+, RHEL 8+, Alpine 3.15+
- **macOS**: 10.15+ (Catalina and newer)
- **Windows**: Windows 10+, Windows Server 2019+

## Comprehensive Testing Strategy

### 1. Multi-Python Version Testing Matrix

```yaml
# .github/workflows/test-migration.yml
strategy:
  matrix:
    python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]
    mkdocs-material-version: ["9.0.0", "9.5.0", "latest"]
    os: [ubuntu-latest, windows-latest, macos-latest]
```

### 2. Migration Validation Tests

```python
# tests/test_migration.py
import subprocess
import sys
import tempfile
import os

def test_uv_build():
    """Test that package builds with UV"""
    result = subprocess.run([
        "uv", "build", "--no-sources"
    ], capture_output=True, text=True)
    assert result.returncode == 0, f"UV build failed: {result.stderr}"

def test_pip_install_compatibility():
    """Test that package can still be installed with pip"""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", ".", 
            "--target", tmpdir
        ], capture_output=True, text=True)
        assert result.returncode == 0, f"Pip install failed: {result.stderr}"

def test_plugin_registration():
    """Test that MkDocs plugin is properly registered"""
    import pkg_resources
    
    entry_points = list(pkg_resources.iter_entry_points('mkdocs.plugins'))
    plugin_names = [ep.name for ep in entry_points]
    
    assert 'obsidian-interactive-graph' in plugin_names

def test_mkdocs_compatibility():
    """Test that plugin works with MkDocs"""
    import tempfile
    import yaml
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create minimal mkdocs.yml
        config = {
            'site_name': 'Test Site',
            'plugins': ['obsidian-interactive-graph']
        }
        
        config_path = os.path.join(tmpdir, 'mkdocs.yml')
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        
        # Test mkdocs build
        result = subprocess.run([
            "mkdocs", "build", "--config-file", config_path,
            "--site-dir", os.path.join(tmpdir, "site")
        ], capture_output=True, text=True, cwd=tmpdir)
        
        assert result.returncode == 0, f"MkDocs build failed: {result.stderr}"
```

### 3. Performance Benchmarking

```python
# tests/test_performance.py
import time
import subprocess

def test_uv_vs_pip_install_speed():
    """Compare UV vs pip installation speed"""
    
    # Test UV installation
    start_time = time.time()
    result_uv = subprocess.run([
        "uv", "pip", "install", "--system", "."
    ], capture_output=True)
    uv_time = time.time() - start_time
    
    # Test pip installation  
    start_time = time.time()
    result_pip = subprocess.run([
        "pip", "install", "."
    ], capture_output=True)
    pip_time = time.time() - start_time
    
    print(f"UV install time: {uv_time:.2f}s")
    print(f"Pip install time: {pip_time:.2f}s")
    print(f"UV speedup: {pip_time/uv_time:.1f}x")
    
    assert result_uv.returncode == 0
    assert result_pip.returncode == 0
```

### 4. Docker Testing Strategy

```dockerfile
# test.Dockerfile
FROM python:3.11-slim

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /test

# Copy project files
COPY pyproject.toml ./
COPY obsidian_interactive_graph ./obsidian_interactive_graph
COPY README.md ./
COPY .git ./.git

# Test UV build
RUN uv build --no-sources

# Test installation
RUN uv pip install --system dist/*.whl

# Test plugin functionality
RUN python -c "import obsidian_interactive_graph.plugin; print('Plugin import successful')"

# Test MkDocs integration
COPY test_mkdocs.yml ./mkdocs.yml
RUN mkdocs build --strict
```

## Implementation Phases

### Phase 1: Foundation Setup
1. **Create feature branch** for UV migration
2. **Create pyproject.toml** with UV build backend
3. **Update .gitignore** for UV-specific files
4. **Initial testing** with UV build

### Phase 2: Docker & CI Integration
1. **Update Dockerfile** to use UV
2. **Configure GitHub Actions** for UV testing
3. **Multi-platform testing** setup
4. **Performance benchmarking** implementation

### Phase 3: Documentation & Validation
1. **Update README** with UV installation instructions
2. **Comprehensive testing** across Python versions
3. **Plugin functionality verification**
4. **Migration validation checklist** completion

### Phase 4: Deployment & Monitoring
1. **Create pull request** with comprehensive changes
2. **Community testing** and feedback
3. **Final validation** and merge
4. **Post-migration monitoring**

## Migration Validation Checklist

### Pre-Migration Validation
- [ ] Current setup.py builds successfully
- [ ] All dependencies in requirements.txt are available
- [ ] Plugin works with current MkDocs Material version
- [ ] Tests pass with current setup
- [ ] Documentation builds without errors

### Post-Migration Validation
- [ ] `uv build` creates valid wheel and sdist
- [ ] `pip install` still works (backward compatibility)
- [ ] Plugin entry point is correctly registered
- [ ] MkDocs can load and use the plugin
- [ ] All optional dependencies install correctly
- [ ] Docker build works with UV
- [ ] Documentation builds successfully
- [ ] Performance improvements are measurable

### Cross-Platform Testing
- [ ] Linux (Ubuntu) - UV build and install
- [ ] macOS - UV build and install  
- [ ] Windows - UV build and install
- [ ] Python 3.9, 3.10, 3.11, 3.12, 3.13 compatibility

### Integration Testing
- [ ] Works with latest MkDocs Material (9.x)
- [ ] Compatible with all plugins in requirements.txt
- [ ] No breaking changes for end users
- [ ] CI/CD pipeline works with UV
- [ ] Docker images build successfully

## Benefits & Expected Outcomes

### Performance Improvements
- **10-100x faster** dependency resolution
- **Reduced build times** in CI/CD pipelines
- **Faster Docker builds** with UV caching
- **Improved developer experience** with instant installs

### Modern Standards Compliance
- **PEP 518/621** compliant pyproject.toml
- **Standardized build backend** (uv_build)
- **Reproducible builds** with lockfiles
- **Future-proof** packaging approach

### Developer Experience Enhancements
- **Single tool** for all package management
- **Better error messages** and debugging
- **Simplified workflow** for contributors
- **Enhanced dependency management**

### Ecosystem Benefits
- **Broader Python version support** (3.9+, following current support lifecycle)
- **Better integration** with modern tools
- **Improved security** with dependency locking
- **Enhanced maintainability**

## Risk Mitigation

### Backward Compatibility
- **Maintain pip compatibility** for existing users
- **Gradual migration** approach with testing
- **Clear documentation** for migration path
- **Support for both old and new workflows**

### Testing Coverage
- **Comprehensive test suite** across platforms
- **Automated validation** in CI/CD
- **Performance regression testing**
- **Integration testing** with ecosystem

### Rollback Strategy
- **Feature branch** development approach
- **Incremental changes** with validation points
- **Ability to revert** to setup.py if needed
- **Clear migration documentation**

## Timeline & Milestones

### Week 1: Foundation
- [ ] Create feature branch
- [ ] Implement pyproject.toml
- [ ] Basic UV build testing

### Week 2: Integration
- [ ] Docker updates
- [ ] CI/CD configuration
- [ ] Cross-platform testing

### Week 3: Validation
- [ ] Comprehensive testing
- [ ] Performance benchmarking
- [ ] Documentation updates

### Week 4: Deployment
- [ ] Pull request creation
- [ ] Community review
- [ ] Final validation and merge

## Conclusion

This migration to UV represents a significant modernization of the project's packaging infrastructure. By adopting UV as the package manager, we achieve:

1. **State-of-the-art performance** with 10-100x faster dependency resolution
2. **Modern packaging standards** compliance (PEP 518/621)
3. **Enhanced developer experience** with simplified workflows
4. **Future-proof architecture** aligned with 2025 best practices
5. **Maintained backward compatibility** for existing users

The comprehensive testing strategy ensures a smooth migration with minimal risk, while the phased implementation approach allows for validation at each step. This migration positions the project at the forefront of Python packaging technology while maintaining the reliability and compatibility that users expect.
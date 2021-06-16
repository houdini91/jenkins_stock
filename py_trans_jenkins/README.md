# Trans jenkins python library

# Install
```
make install_python
```

# Run example
```
python -m "trans_jenkins.examples.simple" collector --token TEST
python -m "trans_jenkins.examples.simple" filter --token TEST
python -m "trans_jenkins.examples.simple" generate
```

# Use library
```
from trans_jenkins.src import pipeline, output
template_pipeline = pipeline.BasePipeline()
output_pipeline = output.Output()
```

# Testing - relative example run
```
cd py_trans_jenkins
python -m "trans_jenkins.examples.simple" collector --token TEST
python -m "trans_jenkins.examples.simple" filter --token TEST
python -m "trans_jenkins.examples.simple" generate
```

# Allowing jenkins to run inline scripts - Use with care - Minimize your setting.
```
System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "sandbox allow-scripts; default-src *; style-src * http://* 'unsafe-inline' 'unsafe-eval'; script-src 'self' http://* 'unsafe-inline' 'unsafe-eval'");
```
## py-trading-tool
Simple trading tool I created to help me make trading decisions

### Packages
https://blog.quantinsti.com/install-ta-lib-python/#macos

Must have homebrew installed

#### Finance
 `pip install yfinance`
 
 TRASH FOR NOW
`pip install zipline`
--zipline dependencies (must install first)
    1st. link python to homebrew
    `brew link python` and choose overwrite option if prompted
   `brew install freetype pkg-config gcc openssl`
--anaconda dependencies for zipline
  create new virtual environment
  `conda create -n env_zipline python=3.5`
   activate it
  `conda activate env_zipline`
   install zipline
   `conda install -c Quantopian zipline`
   END TRASH FOR NOW
   
   `pip install iexfinance`
   `pip install pyEX`
   

#### Tech analysis

`brew install ta-lib`
`pip install ta-lib`

### General tools
`pip install matplotlib` (may be unnecessary)
`pip install numpy`
`pip install pandas`
`pip install pandas-datareader`

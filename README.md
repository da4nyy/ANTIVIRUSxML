

<div align="center">

  <h1>ANTIVIRUSXML</h1>
  
  <p>
      File Integrity Monitor with Malware detection using Machine learning 
      <br>(tested only on linux)
  </p>

  

   

</div>

<br />

<!-- Table of Contents -->
# :notebook_with_decorative_cover: Table of Contents

- [About the Project](#star2-about-the-project)
- [Getting Started](#toolbox-getting-started)
  * [Prerequisites](#bangbang-prerequisites)
  * [Installation](#gear-installation)
- [Usage](#eyes-usage)
- [Contact](#handshake-contact)
- [Acknowledgements](#gem-acknowledgements)
  

<!-- About the Project -->
## :star2: About the Project

Overview
============
This Python project is a project that combine between  :
1. basic file integrity monitor: which it takes two arguments: a directory to scan, and an output file for alerts. The script will recursively scan the given directory and its subdirectories, and will create alerts for any added, removed, or changed files. The script uses the os, sys, and pickle libraries to perform file system operations, as well as the datetime, hashlib, logging, and time libraries for other operations.
2. malware detection using machine learning : it helps train a classifier to be able to detect [PE files](https://en.wikipedia.org/wiki/Portable_Executable) as either malicious or legitimate. It tries out 6 different classification algorithms before deciding which one to use for prediction by comparing their results. 


<div align="center"> 
  <img src="https://user-images.githubusercontent.com/117517618/206859303-8042f133-5fa3-493a-9b3b-b65995f4ecef.png" alt="screenshot" />
</div>








<!-- Getting Started -->
## 	:toolbox: Getting Started

<!-- Prerequisites -->
### :bangbang: Prerequisites

This project uses some libraries that you need to install them first :

```bash
 pip install -r requirements.txt
```

<!-- Installation -->
### :gear: Installation


```bash
  git clone https://github.com/da4nyy/ANTIVIRUSxML/
  cd ANTIVIRUSxML
```


<!-- Run Locally -->
### :running: Run Locally

Clone the project


Go to the project directory

```bash
  cd ANTIVIRUSxML/
```

Install dependencies

```bash
   pip install -r requirements.txt
```

train the model ( you can skip this phase : you already find the files in the classifier directory

```bash
   python3 Malware-detection-learning.py data.csv
```

Start the file monitor and malware detection handler

```bash
   python3 antivirusXml.py -i <input directory to monitor> -o <output file>  
```

<!-- Usage -->
## :eyes: Usage

+ You may monitor the integrity of the files that may have PII. In this case, you can place the script where your files live, and create a crontab or use task scheduler to run the script.
+ You can use the script to monitor the files stored in the web app and scan the added files.
+ If you are in the Blue Team at a CCDC competition, you can use this script to monitor your server and easily see which files modified.



<!-- Roadmap -->
## :compass: Roadmap

* [x] scan x32 PE files
* [ ] scan x64 PE files

<!-- Contributing -->
## :wave: Contributing

<a href="https://github.com/da4nyy/ANTIVIRUSxML/graphs/contributors">

</a>


Contributions are always welcome!


<!-- Contact -->
## :handshake: Contact

kacem hakim - [@DARNY](https://twitter.com/darny74258511) - kacemhakim19@gmail.com

Project Link: [https://github.com/](https://github.com/da4nyy/ANTIVIRUSxML)

<!-- Acknowledgments -->
## :gem: Acknowledgements

 - [kaggle mai dali](https://www.kaggle.com/code/maidaly/malware-detection-with-machine-learning)
 - [Te-k](https://github.com/Te-k)
 - [MaksimEkin- file integrity monitor](https://github.com/MaksimEkin/)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)




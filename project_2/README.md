# Discovering vulnerabilities in JavaScript web applications

JavaScript is the most widely used web programming language among professional and beginner
programmers. In order to develop secure code and avoid exploits, developers require great knowledge on how to surpass and sanitize code vulnerabilities and must be careful in the way information flows through their code. Although many people don’t have this knowledge or just have a complex application whose flows are difficult to follow, there are vulnerability scanning tools available to use.  
So we developed a tool that can **help in identifying dangerous information flows**, which might expose users’ private data to other malicious users

## Details on how the tool works
Further details are found in the group report, under docs with the name [`report`](docs/report.pdf)

## Running the tool
`python Tool.py <path_to_program>.json <path_to_pattern>.json`

## Requirements
Python3
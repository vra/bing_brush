<div align="center">
  <img width="200px" src="https://github.com/vra/bing_brush/blob/main/assets/logo.jpeg"/>
  
### One-line Image Generating Program Based on the Bing Image Createor (Powered by DALL·E 3)

</div>

---

Credit: The solution of invoking Bing Image Creator API is from <https://github.com/acheong08/BingImageCreator>.

## Installation
```bash
pip install bing_brush
```

### Obtain your cookie

The cookie of Bing.com is needed. You need to login to Bing.com first, then follow the steps below to write your cookie to a file (e.g., `cookie.txt`):

#### Step0:
Vist <https://www.bing.com/images/create>
<div align="center">
  <img width="500px" src="https://github.com/vra/bing_brush/blob/main/assets/step0.jpg"/>
</div>

#### Step1:
Press F12 to open dev tools, then refresh the web page to run all requests again:
<div align="center">
  <img width="500px" src="https://github.com/vra/bing_brush/blob/main/assets/step1.jpg"/>
</div>
Select any rquest with type of xhr, then click the head of the request


#### Step2:
In the detail of the request header, find the `Cookie` section, copy the value of it to your file (e.g., cookie.txt)
<div align="center">
  <img width="500px" src="https://github.com/vra/bing_brush/blob/main/assets/step2.jpg"/>
</div>
Then your cookie for Bing.com has successfully be stored.

## Usage
### CLI
```bash
# -c is short for --cookie, -p is short for --prompt
bing_brush -c cookie.txt -p 'a cute panda eating bamboos' -o output_folder
```
### Python API
```python
brush = BingBrush(cookie='/path/to/cookie.txt')
brush.process(prompt='a cute panda eating bamboos', out_folder='output_folder')
```


## TODO
+ [ ] unit test
+ [ ] support for obtaining cookie from os.env


## Logo
Logo of this project is generated by Bing Image, prompt:
> A minimalist logo vector image, square-shaped, with a magical brush implemented in Python language in the center, colorful, digitial art

## Contribution

##

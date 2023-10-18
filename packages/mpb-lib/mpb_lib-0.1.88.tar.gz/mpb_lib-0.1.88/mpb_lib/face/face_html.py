# 助手さんの顔表示クラスで利用するHTML,JavaScriptのテンプレート
# 
# Copyright (c) 2023 Atsush Shibata(shivata@m-info.co.jp)
#
# Released under the MIT license.

HTML_FRAME = """
    <div id="face">
        <div id="left_eyeblow"></div>
        <div id="right_eyeblow"></div>
        <div id="left_eye"></div>
        <div id="right_eye"></div>
        <div id="mouth"></div>
    </div>
"""

WORD = """
    <p class="balloon" id="word"></p>
"""


STYLES = """
<style>
    
    #face {
        background-image:url("https://github.com/shibats/mpb_samples/blob/main/assets/face/assistant_face.png?raw=true");
        width: 330px;
        height: 420px;
        margin-left: -80px;
        margin-top: -100px;
        transform: scale(0.5, 0.5);
    }
    #left_eyeblow {
        background-image:url("https://github.com/shibats/mpb_samples/blob/main/assets/face/eyeblow_l.png?raw=true");
        width: 64px;
        height: 22px;
        position: absolute;
        left: 90px;
        top: 142px;
    }
    #right_eyeblow {
        background-image:url("https://github.com/shibats/mpb_samples/blob/main/assets/face/eyeblow_r.png?raw=true");
        width: 62px;
        height: 20px;
        position: absolute;
        left: 215px;
        top: 140px;
    }
    #left_eye {
        background-image:url("https://github.com/shibats/mpb_samples/blob/main/assets/face/eye_l_1.png?raw=true");
        width: 74px;
        height: 82px;
        position: absolute;
        left: 82px;
        top: 169px;
    }
    #right_eye {
        background-image:url("https://github.com/shibats/mpb_samples/blob/main/assets/face/eye_r_1.png?raw=true");
        width: 66px;
        height: 82px;
        position: absolute;
        left: 210px;
        top: 165px;
    }
    #mouth {
        background-image:url("https://github.com/shibats/mpb_samples/blob/main/assets/face/mouth_1.png?raw=true");
        width: 86px;
        height: 70px;
        position: absolute;
        left: 145px;
        top: 270px;
    }

    .balloon {
        position: absolute;
        display: inline-block;
        margin: 1.5em 0 1.5em 15px;
        padding: 7px 10px;
        min-width: 120px;
        max-width: 95%;
        color: #555;
        font-size: 16px;
        background: #FFF;
        border: solid 3px #555;
        border-radius: 8px;
        box-sizing: border-box;
    }
    .balloon:before {
        content: "";
        position: absolute;
        top: 50%;
        left: -24px;
        margin-top: -12px;
        border: 12px solid transparent;
        border-right: 12px solid #FFF;
        z-index: 2;
    }
    .balloon:after {
        content: "";
        position: absolute;
        top: 50%;
        left: -30px;
        margin-top: -14px;
        border: 14px solid transparent;
        border-right: 14px solid #555;
        z-index: 1;
    }
    p.balloon  {
        margin-left: 200px;
        margin-top: -300px;
        padding: 0.5em;
        font-size: 24pt;
    }
</style>
"""

SCRIPT = """
<script>
    function setBackground(the_id, im) {
     const elementReference = document.querySelector('#'+the_id);
     console.log(elementReference);
     elementReference.style.backgroundImage = "url(https://github.com/shibats/mpb_samples/blob/main/assets/face/"+im+"?raw=true)";
    }

    function setXPosition(the_id, x) {
     const elementReference = document.querySelector('#'+the_id);
     elementReference.style.left = x;
    }


    function setYPosition(the_id, x) {
     const elementReference = document.querySelector('#'+the_id);
     elementReference.style.top = x;
    }


    function rotate(the_id, deg) {
     const elementReference = document.querySelector('#'+the_id);
     elementReference.style.transform = "rotate("+deg+"deg)";
    }
    
    function say(msg) {
     const elementReference = document.querySelector("#word");
     elementReference.innerHTML = msg;

    }

</script>
    
"""

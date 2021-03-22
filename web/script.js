let input = document.getElementById("input");
        let div = document.getElementById("sendAndMicrophone");
        let svg = document.getElementsByTagName("svg");
 
        let command;

        let tts = true;

        var moved = false;

        let done = false;

        let inpt = false;

        let lc = "";

        let more_news;

        let dark = true;

        let speaking = false;

        let sr_input = "";

        let changed = false;

        for (let i = 0; i < svg.length; i++) {
            svg[i].classList.add("dark");
        }

        input.classList.add("dark");

        function toggle_mode() {
            let body = document.getElementsByTagName("body")[0];
            let span = document.getElementsByClassName("span");
            let out = document.getElementsByClassName("out");
            let element = document.getElementById("light-dark");
            let news = document.getElementsByClassName("news");
            if (dark) {
                element.innerHTML = '<svg onclick="toggle_mode();" style="position: fixed; top: 0;" xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-brightness-high" viewBox="0 0 16 16"><path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/></svg>'
                body.style.backgroundColor = "#ffffff";
                for (let i = 0; i < svg.length; i++) {
                    svg[i].classList.remove("dark");
                    svg[i].classList.add("light");
                }
                input.classList.remove("dark");
                input.classList.add("light");
                for (let i = 0; i < span.length; i++) {
                    span[i].classList.remove("in-dark");
                    span[i].classList.add("in-light");
                }
                for (let i = 0; i < out.length; i++) {
                    out[i].classList.remove("out-dark");
                    out[i].classList.add("out-light");
                }
                for (let i = 0; i < news.length; i++) {
                    news[i].classList.remove("news-dark");
                    news[i].classList.add("news-light");
                }
            } else {
                element.innerHTML = '<svg onclick="toggle_mode();" style="position: fixed; top: 0;" xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-moon" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M14.53 10.53a7 7 0 0 1-9.058-9.058A7.003 7.003 0 0 0 8 15a7.002 7.002 0 0 0 6.53-4.47z"/></svg>'
                body.style.backgroundColor = "#000000";
                for (let i = 0; i < svg.length; i++) {
                    svg[i].classList.remove("light");
                    svg[i].classList.add("dark");
                }
                input.classList.remove("light");
                input.classList.add("dark");
                for (let i = 0; i < span.length; i++) {
                    span[i].classList.remove("in-light");
                    span[i].classList.add("in-dark");
                }
                for (let i = 0; i < out.length; i++) {
                    out[i].classList.remove("out-light");
                    out[i].classList.add("out-dark");
                }
                for (let i = 0; i < news.length; i++) {
                    news[i].classList.remove("news-light");
                    news[i].classList.add("news-dark");
                }
            }
            dark = !dark;
            eel.toggle_mode()()
        }

        eel.expose(update_news);
        function update_news(news) {
            more_news = news;
        }

        function expand() {
            let element_div = document.getElementsByClassName('more')[document.getElementsByClassName('more').length - 1];
            if (!dark) {
                more_news = more_news.replaceAll("news-dark", "news-light");
            }
            console.log(more_news);
            element_div.innerHTML = more_news;
        }

        document.onmousemove = function(e) {
            if (!moved) {
                moved = true;
                get_answer();
            }
        }

        $.ajax({
            url: "https://geolocation-db.com/jsonp",
            jsonpCallback: "callback",
            dataType: "jsonp",
            success: function(location) {
                lc = location.city + ", " + location.country_name;
            }
        });

        eel.expose(get_input);
        function get_input() {
            inpt = true;
        }

        eel.expose(get_location);
        function get_location() {
            return lc;
        }

        input.onkeyup = async function(e) {
            done = false;
            get_answer();
            if (!e) e = window.event;
            var keyCode = e.code || e.key;
            if (keyCode == "Enter") {
                if (inpt) {
                    done = true;
                } else {
                    send(input.value);
                }
            }
            if (input.value != "") {
                let sr = document.getElementById("sr");
                for (let i = 0; i <= 9; i++) {
                    sr.style.padding = "1" + i + "px";
                    await new Promise(r => setTimeout(r, 10));
                }
                div.innerHTML = '<svg style="margin-left: 88%; width: 11%;" xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16" onclick="send(input.value);" id="send"><path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/></svg>';
                for (let i = 0; i < svg.length; i++) {
                    if (dark) {
                        svg[i].classList.add("dark");
                    } else {
                        svg[i].classList.add("light");
                    }
                }
            } else {
                let send = document.getElementById("send");
                for (let i = 0; i <= 9; i++) {
                    send.style.padding = "1" + i + "px";
                    await new Promise(r => setTimeout(r, 10));
                }
                div.innerHTML = '<svg id="sr" onclick="sr();" style="margin-left: 88%; width: 11%;" xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-mic" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1a5 5 0 0 1-4.5 4.975V15h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3v-2.025A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5z"/><path fill-rule="evenodd" d="M10 8V3a2 2 0 1 0-4 0v5a2 2 0 1 0 4 0zM8 0a3 3 0 0 0-3 3v5a3 3 0 0 0 6 0V3a3 3 0 0 0-3-3z"/></svg>';
                for (let i = 0; i < svg.length; i++) {
                    if (dark) {
                        svg[i].classList.add("dark");
                    } else {
                        svg[i].classList.add("light");
                    }
                }
            }
        }

        input.onblur = function() {
            get_answer();
        }
        input.onfocus = function() {
            get_answer();
        }

        async function send(command) {
            if (!inpt) {
                if (command != "") {
                    input.value = "";
                    let question, greeting, about_themselves, statement, about_it, greeting_word
                    let user_input_without_syntax = await eel.remove_syntax(command)();
                    question_GUI(command);
                    let temp = await eel.generate_answer(command, user_input_without_syntax)();
                }
            } else {
                done = true;
            }
        }
        async function question_GUI(command) {
            let br = document.createElement("br");
            br.style.clear = "both";
            document.body.appendChild(br);
            let question_GUI = document.createElement("span");
            if (dark) {
                question_GUI.classList.add("in-dark");
            } else {
                question_GUI.classList.add("in-light");
            }
            question_GUI.classList.add("span");
            if (input.type == "text") {
                question_GUI.innerHTML = command;
            } else {
                let string = "";
                for (let i = 0; i < command.length; i++) {
                    string += "•";
                }
                input.type = "text";
                question_GUI.innerHTML = string;
            }
            document.body.appendChild(question_GUI);
            for (let i = 30; i >= 10; i--) {
                question_GUI.style.padding = i + "px" + " 20px 10px 18px";
                await new Promise(r => setTimeout(r, 1));
            }
            window.scrollTo(0, document.body.scrollHeight);
            await get_answer()
        }
        async function get_answer() {
            await new Promise(r => setTimeout(r, 1000));
            let response = await eel.send_to_js()();
            let answer = response[0];
            console.log(answer);
            if (response[1]) {
                if (tts) {
                    toggle_tts();
                    eel.toggle_tts();
                }
            }
            if (answer != "") {
                let br = document.createElement("br");
                br.style.clear = "both";
                document.body.appendChild(br);
                answer_GUI = document.createElement("span");
                answer_GUI.classList.add("out");
                if (dark) {
                    answer_GUI.classList.add("out-dark");
                } else {
                    answer_GUI.classList.add("out-light");
                }
                answer_GUI.innerHTML = answer;
                answer_GUI.style.borderRadius = "25px 25px 25px 5px";
                answer_GUI.style.padding = "10px 20px 10px 18px";
                document.body.appendChild(answer_GUI);
                eel.done();
                for (let i = 30; i >= 10; i--) {
                    answer_GUI.style.padding = i + "px" + " 20px 10px 18px";
                    await new Promise(r => setTimeout(r, 1));
                }
                if (answer == "Please, type in your password") {
                    input.type = "password";
                }
                window.scrollTo(0, document.body.scrollHeight);
            }
        }

        function toggle_tts() {
            let tts_button = document.getElementById("toggle_tts");
            if (tts) {
                tts_button.innerHTML = '<path d="M6.717 3.55A.5.5 0 0 1 7 4v8a.5.5 0 0 1-.812.39L3.825 10.5H1.5A.5.5 0 0 1 1 10V6a.5.5 0 0 1 .5-.5h2.325l2.363-1.89a.5.5 0 0 1 .529-.06zM6 5.04L4.312 6.39A.5.5 0 0 1 4 6.5H2v3h2a.5.5 0 0 1 .312.11L6 10.96V5.04zm7.854.606a.5.5 0 0 1 0 .708L12.207 8l1.647 1.646a.5.5 0 0 1-.708.708L11.5 8.707l-1.646 1.647a.5.5 0 0 1-.708-.708L10.793 8 9.146 6.354a.5.5 0 1 1 .708-.708L11.5 7.293l1.646-1.647a.5.5 0 0 1 .708 0z"/>';
                tts = false;
                for (let i = 0; i < svg.length; i++) {
                    if (dark) {
                        svg[i].classList.add("dark");
                    } else {
                        svg[i].classList.add("light");
                    }
                }
            } else {
                tts_button.innerHTML = '<path d="M11.536 14.01A8.473 8.473 0 0 0 14.026 8a8.473 8.473 0 0 0-2.49-6.01l-.708.707A7.476 7.476 0 0 1 13.025 8c0 2.071-.84 3.946-2.197 5.303l.708.707z"/><path d="M10.121 12.596A6.48 6.48 0 0 0 12.025 8a6.48 6.48 0 0 0-1.904-4.596l-.707.707A5.483 5.483 0 0 1 11.025 8a5.483 5.483 0 0 1-1.61 3.89l.706.706z"/><path d="M10.025 8a4.486 4.486 0 0 1-1.318 3.182L8 10.475A3.489 3.489 0 0 0 9.025 8c0-.966-.392-1.841-1.025-2.475l.707-.707A4.486 4.486 0 0 1 10.025 8zM7 4a.5.5 0 0 0-.812-.39L3.825 5.5H1.5A.5.5 0 0 0 1 6v4a.5.5 0 0 0 .5.5h2.325l2.363 1.89A.5.5 0 0 0 7 12V4zM4.312 6.39L6 5.04v5.92L4.312 9.61A.5.5 0 0 0 4 9.5H2v-3h2a.5.5 0 0 0 .312-.11z"/>';
                tts = true;
                for (let i = 0; i < svg.length; i++) {
                    if (dark) {
                        svg[i].classList.add("dark");
                    } else {
                        svg[i].classList.add("light");
                    }
                }
            }
            eel.toggle_tts();
        }

        eel.expose(send_input_value);
        function send_input_value() {
            if (!changed) {
                sendAndMicrophone.innerHTML = '<svg id="sr" onclick="sr();" xmlns="http://www.w3.org/2000/svg" style="margin-left: 88%; width: 11%;" width="50" height="50" fill="currentColor" class="bi bi-mic" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1a5 5 0 0 1-4.5 4.975V15h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3v-2.025A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5z"/><path fill-rule="evenodd" d="M10 8V3a2 2 0 1 0-4 0v5a2 2 0 1 0 4 0zM8 0a3 3 0 0 0-3 3v5a3 3 0 0 0 6 0V3a3 3 0 0 0-3-3z"/></svg>';
                for (let i = 0; i < svg.length; i++) {
                    if (dark) {
                        svg[i].classList.add("dark");
                    } else {
                        svg[i].classList.add("light");
                    }
                }
                changed = true;
            }
            let value = input.value;
            if (!speaking) {
                if (value != "") {
                    if (done) {
                        question_GUI(value);
                        input.value = "";
                        inpt = false;
                        done = false;
                        changed = false;
                        return value;
                    }
                }
            } else {
                if (sr_input != "") {
                    question_GUI(sr_input);
                    input.value = "";
                    inpt = false;
                    done = false;
                    changed = false;
                    return sr_input;
                }
            }
        }
        
        function sr() {
            let sendAndMicrophone = document.getElementById("sendAndMicrophone");
            var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
            var recognition = new SpeechRecognition();
        
            // This runs when the speech recognition service starts
            recognition.onstart = function() {
                sr_input = "";
                let audio = new Audio("sound.mp3");
                audio.play();
                sendAndMicrophone.innerHTML = '<svg id="sr" onclick="sr();" xmlns="http://www.w3.org/2000/svg" style="margin-left: 88%; width: 11%;" width="50" height="50" fill="currentColor" class="bi bi-mic-fill" viewBox="0 0 16 16"><path d="M5 3a3 3 0 0 1 6 0v5a3 3 0 0 1-6 0V3z"/><path fill-rule="evenodd" d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1a5 5 0 0 1-4.5 4.975V15h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3v-2.025A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5z"/></svg>';
                for (let i = 0; i < svg.length; i++) {
                    if (dark) {
                        svg[i].classList.add("dark");
                    } else {
                        svg[i].classList.add("light");
                    }
                }
                speaking = true;
            };
            
            recognition.onspeechend = function() {
                recognition.stop();
                sendAndMicrophone.innerHTML = '<svg id="sr" onclick="sr();" xmlns="http://www.w3.org/2000/svg" style="margin-left: 88%; width: 11%;" width="50" height="50" fill="currentColor" class="bi bi-mic" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1a5 5 0 0 1-4.5 4.975V15h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3v-2.025A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5z"/><path fill-rule="evenodd" d="M10 8V3a2 2 0 1 0-4 0v5a2 2 0 1 0 4 0zM8 0a3 3 0 0 0-3 3v5a3 3 0 0 0 6 0V3a3 3 0 0 0-3-3z"/></svg>';
                for (let i = 0; i < svg.length; i++) {
                    if (dark) {
                        svg[i].classList.add("dark");
                    } else {
                        svg[i].classList.add("light");
                    }
                }
            }
            
            // This runs when the speech recognition service returns result
            recognition.onresult = function(event) {
                command = event.results[0][0].transcript;
                input.value = command;
                sr_input = command;
                speaking = false;
                if (!inpt) send(command);
                else {
                    input.value = command;
                    sendAndMicrophone.innerHTML = '<svg style="margin-left: 88%; width: 11%;" xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16" onclick="send(input.value);" id="send"><path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/></svg>';
                    for (let i = 0; i < svg.length; i++) {
                        if (dark) {
                            svg[i].classList.add("dark");
                        } else {
                            svg[i].classList.add("light");
                        }
                    }
                }
            };
            
            // start recognition
            recognition.start();
        }

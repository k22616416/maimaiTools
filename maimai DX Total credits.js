javascript: (function () {
    if (['maimaidx-eng.com'].indexOf(document.location.host) < 0) {
        alert("此工具需要在maimai DX-NET的頁面下才能運作");
        return;
    }
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "https://maimaidx-eng.com/maimai-mobile/record/", true);
    xhr.responseType = "document";
    xhr.onload = function () {
        if (!(xhr.status >= 200 && xhr.status <= 299))
            return;
        var todayRecords = Array();
        var credits = 0;
        for (let i of xhr.responseXML.getElementsByClassName("p_10 t_l f_0 v_b")) {
            var trackStr = i.getElementsByClassName("sub_title t_c f_r f_11")[0].getElementsByClassName("v_b")[0].innerHTML
            var timeStr = i.getElementsByClassName("sub_title t_c f_r f_11")[0].getElementsByClassName("v_b")[1].innerHTML;
            var trackTime = new Date(timeStr);
            if (trackTime == NaN) {
                continue;
            }

            trackTime.setHours(trackTime.getHours() - 1);
            if (trackTime.getDate() == new Date().getDate()) {
                var obj = {
                    Track: trackStr,
                    Time: timeStr
                };
                todayRecords.push(obj);
            }
        }
        for (let i = 0; i < todayRecords.length; i++) {
            let n = parseInt(todayRecords[i].Track[7]);
            credits++;
            i += n - 1;
        }
        var msg = new Date().toLocaleDateString('zh-TW') +
            "\nTracks:" + todayRecords.length +
            "\n你今天打了" + credits + "道\n"
            + "金額為:" + credits * 30 + "元";
        console.log(msg);
        var msgDiv = xhr.responseXML.createElement("div");
        msgDiv.innerHTML = msg;
        msgDiv.setAttribute('class', 'wrapper t_c');
        msgDiv.setAttribute('style', "background-color: yellow;");
        document.getElementsByClassName("wrapper t_c")[0].appendChild(msgDiv);

    };
    xhr.send();
})();
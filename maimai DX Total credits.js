javascript: (function () {
    // if (['maimaidx-eng.com'].indexOf(document.location.host) < 0) {
    //     alert("此工具需要在maimai DX-NET的頁面下才能運作");
    //     return;
    // }
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "https://maimaidx-eng.com/maimai-mobile/record/", true);
    xhr.responseType = "document";
    xhr.onload = function () {
        if (!(xhr.status >= 200 && xhr.status <= 299))
            return;
        var totalTracks = Array();
        var totalCredits = Array();
        var credits = 0;
        var compTime = new Date();
        for (let i of xhr.responseXML.getElementsByClassName("p_10 t_l f_0 v_b")) {
            var trackStr = i.getElementsByClassName("sub_title t_c f_r f_11")[0].getElementsByClassName("v_b")[0].innerHTML
            var timeStr = i.getElementsByClassName("sub_title t_c f_r f_11")[0].getElementsByClassName("v_b")[1].innerHTML;
            var trackTime = new Date(timeStr);
            if (trackTime == NaN) {
                continue;
            }

            trackTime.setHours(trackTime.getHours() - 1);
            var obj = {
                Track: trackStr,
                Time: timeStr
            };
            totalTracks.push(obj);

            // if (trackTime.getDate() == compTime.getDate()) {
            //     var obj = {
            //         Track: trackStr,
            //         Time: timeStr
            //     };
            //     totalTracks.push(obj);
            // }
            // else {
            //     compTime = new Date(timeStr);
            //     var obj = {
            //         Track: trackStr,
            //         Time: timeStr
            //     };
            //     totalTracks.push(obj);
            // }
        }
        for (let i = 0; i < totalTracks.length; i++) {
            if (new Date(totalTracks[i].Time).getDate() != compTime.getDate()) {
                totalCredits.push({
                    Date: totalTracks[i].Time,
                    Credits: credits
                });
                credits = 0;
                compTime = new Date(totalTracks[i].Time);
            }
            let n = parseInt(totalTracks[i].Track[7]);
            credits++;
            i += n - 1;
        }
        var msg = '';
        for (let i = 0; i < totalCredits.length; i++) {
            let dt = new Date(totalCredits[i].Time);
            msg += "你" + dt.toLocaleDateString('zh-TW') +
                "打了" + totalCredits[i].Credits + "道\n"
                + "金額為:" + totalCredits[i].Credits * 30 + "元";
        }
        // var msg = new Date().toLocaleDateString('zh-TW') +
        //     "\nTracks:" + totalTracks.length +
        //     "\n你今天打了" + credits + "道\n"
        //     + "金額為:" + credits * 30 + "元";
        console.log(msg);
        var msgDiv = xhr.responseXML.createElement("div");
        msgDiv.innerHTML = msg;
        msgDiv.setAttribute('class', 'wrapper t_c');
        msgDiv.setAttribute('style', "background-color: yellow;");
        document.getElementsByClassName("wrapper t_c")[0].appendChild(msgDiv);
    };
    xhr.send();
})();
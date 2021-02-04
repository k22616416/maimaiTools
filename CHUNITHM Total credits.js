javascript: (function () {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "https://chunithm-net-eng.com/mobile/record/playlog", true);
    xhr.responseType = "document";
    xhr.onload = function () {
        if (!(xhr.status >= 200 && xhr.status <= 299))
            return;
        var totalTracks = Array();
        var totalCredits = Array();


        for (let i of xhr.responseXML.getElementsByClassName("frame02 w400")) {
            //var trackStr = i.getElementsByClassName("play_data_side")[0].getElementsByClassName("v_b")[0].innerHTML
            var trackInfo = {
                Time:i.getElementsByClassName("play_datalist_date")[0].innerHTML,
                Image:null,
                Track:i.getElementsByClassName("play_data_side")[0].getElementsByClassName("box02 play_track_block")[0].getElementsByClassName("play_track_text")[0].innerHTML,
                Level:i.getElementsByClassName("play_data_side")[0].getElementsByClassName("box02 play_track_block")[0].getElementsByClassName("play_track_result")[0].children[0].getAttribute("src"),
                // 110/02/05                
            }
            
            
            i.getElementsByClassName("play_data_side")[0];
            // var timeStr = i.getElementsByClassName("play_datalist_date")[0].innerHTML;
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
        }
        var compTime = new Date(totalTracks[0].Time);
        var credits = 0;
        totalCredits.push({
            Date: totalTracks[0].Time,
            Credits: credits
        });
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
            totalCredits[totalCredits.length - 1].Credits++;
            i += n - 1;
        }
        var msg = '目前的Records資料顯示：\n';
        for (let i = 0; i < totalCredits.length; i++) {
            let dt = new Date(totalCredits[i].Date);
            msg += "你" + dt.toLocaleDateString('zh-TW') +
                " 打了" + totalCredits[i].Credits + "道 "
                + "金額為：" + totalCredits[i].Credits * 30 + "元\n";
        }
        console.log(msg);
        console.log("Power by k22616416.");
        var msgDiv = xhr.responseXML.createElement("div");
        msgDiv.innerHTML = msg.replace(/[\n]/g, "<br>");    //Regular Expression
        msgDiv.setAttribute('class', 'wrapper t_c');
        msgDiv.setAttribute('style', "background-color: yellow;text-align: left;font-family:'Times New Roman', Times, serif;");
        document.getElementsByClassName("wrapper t_c")[0].appendChild(msgDiv);
    };
    xhr.send();
})();
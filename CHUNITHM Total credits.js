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
            var trackInfo = {
                Time: i.getElementsByClassName("play_datalist_date")[0].innerHTML,
                Image: null,
                Track: i.getElementsByClassName("play_data_side")[0].getElementsByClassName("play_track_block")[0].getElementsByClassName("play_track_text")[0].innerHTML,
                Level: i.getElementsByClassName("play_data_side")[0].getElementsByClassName("play_track_block")[0].getElementsByClassName("play_track_result")[0].children[0].getAttribute("src"),
                SongTitle: i.getElementsByClassName("play_data_side")[0].getElementsByClassName("box02 play_musicdata_block")[0].getElementsByClassName("play_musicdata_title")[0].innerHTML,

                Score: i.getElementsByClassName("play_data_side")[0].getElementsByClassName("box02 play_musicdata_block")[0].getElementsByClassName("play_musicdata_score clearfix")[0].getElementsByClassName("play_musicdata_score_text")[0].innerHTML
            }
            trackInfo.Score = trackInfo.Score.replace("Score：");
            console.log(trackInfo);
            totalTracks.push(trackInfo);
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
            let n = parseInt(totalTracks[i].Track[6]);
            totalCredits[totalCredits.length - 1].Credits++;
            i += n - 1;
            // console.log(totalTracks[i].Time);
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
        msgDiv.setAttribute('style', "background-color: aqua;text-align: left;font-family:'Times New Roman', Times, serif;");
        document.getElementById("wrap").insertBefore(msgDiv, document.getElementById("inner"));
    };
    xhr.send();
})();
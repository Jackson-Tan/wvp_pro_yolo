<template>
    <div id="yoloPlayer" ref="container">
        <img :src="yoloSrc" id="yoloPlayerBox">
    </div>
</template>

<script>
import axios from "axios";
export default {

    name: 'yoloView',
    props: ['videoUrl', 'error', 'hasaudio'],
    mounted() {
        let paramUrl = decodeURIComponent(this.$route.params.url)
        this.$nextTick(() => {
            if (typeof (this.videoUrl) == "undefined") {
                this.videoUrl = paramUrl;
            }

            console.log("初始化时的地址为: " + this.videoUrl)
            this.yoloSrc = this.video_Yolourl + 'rtmp' + "?url=" + this.videoUrl
            console.log("yolo请求地址为：" + this.yoloSrc);


        })
            // this.playYolo();
    },
    data() {
        return {
            yoloSrc: '',
            baseUrl: 'http://127.0.0.1:5002',
            video_Yolourl: 'http://127.0.0.1:5002/',
            stopUrl: ''

        }
    },
    methods: {
        pause: function () {
            this.yoloSrc = ''
            this.stopUrl = this.baseUrl + '/stop'
            axios({
                method: 'POST',
                url: this.stopUrl
            })
                .then((res) => {
                    console.log(res.data['message']);
                })
                .catch((err) => console.error('Error stopping yolo:', err))
        },

        updatePlayerDomSize() {
            let dom = this.$refs.container;
            let width = dom.parentNode.clientWidth
            let height = (9 / 16) * width

            const clientHeight = Math.min(document.body.clientHeight, document.documentElement.clientHeight)
            if (height > clientHeight) {
                height = clientHeight
                width = (16 / 9) * height
            }

            dom.style.width = width + 'px';
            dom.style.height = height + "px";
        },

        playYolo: function () {
            axios({
                method: 'GET',
                url: this.video_Yolourl + 'rtmp',
                params: {
                    url: this.videoUrl
                }

            })
                .then((res) => {

                    console.log("YOLO分析完成");
                })
                .catch((err) => console.error('Error fetching video stream:', err))
        }
    }

}
</script>

<style>
#yoloPlayer {
    width: 100%;
    height: 100%;
}

#yoloPlayerBox {
    width: 100%;
    max-height: 60vh;
    background-color: #000;
}
</style>
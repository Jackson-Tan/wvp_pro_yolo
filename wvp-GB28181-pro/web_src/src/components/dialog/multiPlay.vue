<template>
    <div id="multiPlayer" style="width: 80%;">
        <el-dialog :visible.sync="dialogFormVisible">
            <el-container>
                <el-main style="padding: 0;">
                    <div style="width: 99%;height: 85vh;display: flex;flex-wrap: wrap;background-color: #000;">
                        <div v-for="i in spilt" :key="i" class="play-box" :style="liveStyle"
                            :class="{ redborder: playerIdx == (i - 1) }" @click="playerIdx = (i - 1)">
                            <div v-if="!rtmp_list[i - 1]" style="color: #ffffff;font-size: 30px;font-weight: bold;">{{ i }}
                            </div>
                            <yoloPlayer ref="player" v-else :videoUrl="rtmp_list[i - 1]"  fluent autoplay @destroy="destroy" />
                        </div>
                    </div>
                </el-main>
            </el-container>
        </el-dialog>

    </div>
</template>

<script>
import yoloPlayer from '../dialog/yoloView.vue'
import player from '../common/jessibuca.vue';
export default {
    name: 'multuPlayer',
    components: { yoloPlayer, player },
    mounted() {
        this.getRtmpUrl();
    },
    props: ["rtmp_list"],
    data() {
        return {
            videoUrl: [],
            spilt: 4,//分屏
            playerIdx: 0,//激活播放器

            updateLooper: 0, //数据刷新轮训标志
            count: 15,
            total: 0,
            currentPage:1,
			count:15,
            //channel
            loading: false,
            dialogFormVisible: false,
        }
    },

    computed: {
        liveStyle() {
            let style = { width: '100%', height: '100%' }
            switch (this.spilt) {
                case 4:
                    style = { width: '49%', height: '49%' }
                    break
                case 9:
                    style = { width: '32%', height: '32%' }
                    break
            }
            this.$nextTick(() => {
                for (let i = 0; i < this.spilt; i++) {
                    const yoloPlayer = this.$refs.yoloPlayer
                    yoloPlayer && yoloPlayer[i] && yoloPlayer[i].updatePlayerDomSize()
                }
            })
            return style
        }
    },

    watch: {
        spilt(newValue) {
            console.log("切换画幅;" + newValue)
            let that = this
            for (let i = 1; i <= newValue; i++) {
                if (!that.$refs['yoloPlayer' + i]) {
                    continue
                }
                this.$nextTick(() => {
                    if (that.$refs['yoloPlayer' + i] instanceof Array) {
                        that.$refs['yoloPlayer' + i][0].resize()
                    } else {
                        that.$refs['yoloPlayer' + i].resize()
                    }
                })

            }
            window.localStorage.setItem('split', newValue)
        },
    },

    destroyed() {
        clearTimeout(this.updateLooper);
    },

    methods: {
        open () { // 在父组件调用打开
            this.dialogFormVisible = true
            this.getRtmpUrl();

        },
        
        getRtmpUrl: function () {
            
            this.$axios({
                method: 'get',
                url: `/api/proxy/list`,
                params: {
                    page: this.currentPage,
                    count: this.count
                }
            }).then(function (res) {
                if (res.data.code === 0) {
                    for (let i = 0; i < res.data.data.list.length; i++) {
                        this.rtmp_list.push(res.data.data.list[i]['dstUrl'])
                    }
                }
                console.log(this.rtmp_list);
                
            }).catch(function (error) {
                console.log(error);
            });
        },

        destroy(idx) {
            console.log(idx);
            this.clear(idx.substring(idx.length - 1))
        },
        clear(idx) {
            let dataStr = window.localStorage.getItem('playData') || '[]'
            let data = JSON.parse(dataStr);
            data[idx - 1] = null;
            console.log(data);
            window.localStorage.setItem('playData', JSON.stringify(data))
        },
    }
}
</script>


<style>
.btn {
    margin: 0 10px;

}

.btn:hover {
    color: #409EFF;
}

.btn.active {
    color: #409EFF;

}

.redborder {
    border: 2px solid red !important;
}

.play-box {
    background-color: #000000;
    border: 2px solid #505050;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
<style>
.videoList {
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
}

.video-item {
    position: relative;
    width: 15rem;
    height: 10rem;
    margin-right: 1rem;
    background-color: #000000;
}

.video-item-img {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
    width: 100%;
    height: 100%;
}


.video-item-title {
    position: absolute;
    bottom: 0;
    color: #000000;
    background-color: #ffffff;
    line-height: 1.5rem;
    padding: 0.3rem;
    width: 14.4rem;
}

.baidumap {
    width: 100%;
    height: 100%;
    border: none;
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    margin: auto;
}

/* 去除百度地图版权那行字 和 百度logo */
.baidumap>.BMap_cpyCtrl {
    display: none !important;
}

.baidumap>.anchorBL {
    display: none !important;
}
</style>
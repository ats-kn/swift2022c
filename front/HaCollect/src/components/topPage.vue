<template>
    <div class="hello">
        <!-- 投稿の情報(fire_data)をitemの変数に格納    item: {TwitterとInstaでキーの数が違ったり、キーはたくさんあるからRealtime databaseで確認してくれ} -->
        <div class="infomation" v-for="(item, post_index) in fire_data">
            <!-- 表示する投稿の数だけ表示（最初はmax=30件表示） -->
            <template v-if="post_index < max">
                <!-- <p>{{post_index}}</p> -->
                <div class="item">

                    <!-- ツイッターの投稿の表示 -->
                    <template v-if="item.SNS_type == 'Twitter'">
                        <div class="card_All">
                            <div class="card_Info">
                                <a v-bind:href=item.link target="_blank" class="card_Link"
                                    rel="noopener noreferrer"><img src="../assets/TwitterIcon.png" /></a>
                                <!-- リンク -->
                                <p class="card_Date">{{ item.date3 }}</p>
                            </div>
                            <!-- 画像情報 -->
                            <!-- 画像や動画があるかチェック -->
                            <template v-if="item.media != null">
                                <!-- urlの情報(item.media)をurlの変数に格納     url: { url0 {media_type: メディアの種類,   media_url:メディアのURL},    url1 {media_type: メディアの種類,   media_url:メディアのURL} .....}となっている -->
                                <template v-for="(url, url_name) in item.media">
                                    <!-- urlのキー名(url0,url1)のうち一つを表示する。（最初はurl0を表示） -->
                                    <template v-if="url_name == 'url' + page[post_index]">
                                        <!-- 動画かどうかチェック -->
                                        <template v-if="url.media_type == 'video'">
                                            <video class="card_Movie" v-bind:src="url.media_url" controls></video>
                                        </template>
                                        <!-- 画像だったら以下実行 -->
                                        <template v-else>
                                            <img class="card_Image" v-bind:src=url.media_url>
                                        </template>
                                    </template>
                                </template>

                                <!-- 画像スライダーのボタン(Twitter) -->
                                <div class="btn-box">
                                    <!-- 表示されている画像が1枚目以降の時、前へボタンを表示 -->
                                    <template v-if="page[post_index] > 0">
                                        <img class="left-btn" @click="prevPage(post_index)"
                                            src="../assets/imageButton_before.png" />
                                    </template>
                                    <!-- 各投稿の最大画像枚数に達するまで、次へボタンを表示 -->
                                    <template v-if="page[post_index] < getObjLength(item.media) - 1">
                                        <img class="right-btn" @click="nextPage(post_index)"
                                            src="../assets/imageButton_after.png" />
                                    </template>
                                </div>
                            </template>

                            <!-- テキスト情報 -->
                            <div class="ac-box">
                                <input :id="[post_index]" name="accordion-1" type="checkbox" />
                                <p class="card_Text">{{ item.text }}</p> <!-- テキスト(最初の文のみプレビュー) -->
                                <a v-bind:href=item.link target="_blank" class="card_LinkText"
                                    rel="noopener noreferrer">投稿元のサイトでこの投稿を見る</a>
                                <!-- テキストでのリンク -->
                                <label :for="[post_index]"></label>
                            </div>
                        </div>
                    </template> <!-- Twitter投稿の終わり -->

                    <!-- インスタグラムの投稿の表示 -->
                    <template v-if="item.SNS_type == 'Instagram'">
                        <div class="card_All">
                            <div class="card_Info">
                                <a v-bind:href=item.link target="_blank" class="card_Link"
                                    rel="noopener noreferrer"><img src="../assets/InstagramIcon.png" /></a>
                                <!-- リンク -->
                                <p class="card_Date">{{ item.date3 }}</p>
                            </div>
                            <!-- 画像情報 -->
                            <!-- 画像や動画があるかチェック -->
                            <template v-if="item.media_type != null">
                                <!-- その投稿が1枚の画像or動画のみだったら    CAROUSEL_ALBUM：複数メディアが含まれている状態  -->
                                <template v-if="item.media_type != 'CAROUSEL_ALBUM'">
                                    <!-- そのメディアが動画だったら -->
                                    <template v-if="item.media_type == 'VIDEO'">
                                        <video class="card_Movie" v-bind:src="item.media_url" controls></video>
                                    </template>
                                    <!-- そのメディアが画像だったら -->
                                    <template v-else>
                                        <img class="card_Image" v-bind:src=item.media_url> <!-- 画像のurl -->
                                    </template>
                                </template>

                                <!-- その投稿が複数メディアある投稿だったら  -->
                                <template v-else>
                                    <!-- urlの情報(item.media)をurlの変数に格納     url: { url0 {media_type: メディアの種類,   media_url:メディアのURL},    url1 {media_type: メディアの種類,   media_url:メディアのURL} .....}となっている -->
                                    <template v-for="(url, url_name) in item.media">
                                        <!-- urlのキー名(url0,url1)のうち一つを表示する。（最初はurl0を表示） -->
                                        <template v-if="url_name == 'url' + page[post_index]">
                                            <!-- 動画かどうかチェック -->
                                            <template v-if="url.media_type == 'VIDEO'">
                                                <video class="card_Movie" v-bind:src="url.media_url" controls></video>
                                            </template>
                                            <!-- 画像だったら以下実行 -->
                                            <template v-else>
                                                <img class="card_Image" v-bind:src=url.media_url> <!-- 画像のurl -->
                                            </template>
                                        </template>
                                    </template>

                                    <!-- 画像スライダーのボタン(Instagram) -->
                                    <div class="btn-box">
                                        <!-- 表示されている画像が1枚目以降の時、前へボタンを表示 -->
                                        <template v-if="page[post_index] > 0">
                                            <img class="left-btn" @click="prevPage(post_index)"
                                                src="../assets/imageButton_before.png" />
                                        </template>
                                        <!-- 各投稿の最大画像枚数に達するまで、次へボタンを表示 -->
                                        <template v-if="page[post_index] < getObjLength(item.media) - 1">
                                            <img class="right-btn" @click="nextPage(post_index)"
                                                src="../assets/imageButton_after.png" />
                                        </template>
                                    </div>
                                </template>
                            </template>

                            <!-- テキスト情報 -->
                            <div class="ac-box">
                                <input :id="[post_index]" name="accordion-1" type="checkbox" />
                                <p class="card_Text">{{ item.text }}</p> <!-- テキスト(最初の文のみプレビュー) -->
                                <a v-bind:href=item.link target="_blank" class="card_LinkText"
                                    rel="noopener noreferrer">投稿元のサイトでこの投稿を見る</a>
                                <!-- テキストでのリンク -->
                                <label :for="[post_index]"></label>
                            </div>
                        </div>
                    </template> <!-- Instagram投稿の終わり -->

                </div>
            </template>
        </div>
    </div>

    <div class="Hello2">
        <!-- 投稿表示限界数(fire_data.length)に達するまでmoreボタンを表示 -->
        <template v-if="max < fire_data.length">
            <!-- <p>{{max}}</p> -->
            <p class="button_More" v-on:click="displayMore">more</p>
        </template>
    </div>
</template>



<script>
export default {
    name: "topPage",
    data() {
        return {
            max: this.$store.state.posts_num,  //表示する投稿数
            page: this.InitializeArray(this.$store.state.get_posts_num)   //urlの番号を格納する配列？
        }
    },
    methods: {
        // 画像スライダーの一つ次の画像に移る関数
        nextPage(post_index) {
            // console.log(post_index)
            this.page[post_index]++;
        },
        // 画像スライダーの一つ前の画像に移る関数
        prevPage(post_index) {
            // console.log(post_index)
            this.page[post_index]--;
        },
        // 投稿の表示数を増やす関数        
        displayMore() {
            this.max += this.$store.state.posts_num
        },
        // オブジェクトに含まれるキーの数を返す関数
        getObjLength(obj) {
            // console.log(Object.keys(obj).length)
            return Object.keys(obj).length
        },
        // 配列を作ってくれる関数
        InitializeArray(num) {
            let array = Array(num)
            array.fill(0)
            // console.log(array)
            return array
        }
    },
    computed: {
        fire_data: function () {
            return this.$store.state.top_fire_data   //store.jsのstateを参照
        },
    },
};
</script>



<style scoped>
.hello {
    padding-top: 80px;
}

.infomation {
    display: inline-block;
    /* width: 30%; */
}

.item {
    display: flex;
    flex-wrap: wrap;
}

.card_All {
    position: relative;
    overflow: hidden;
    float: left;
    width: 100%;
    height: auto;
    background: #ffffff;
    border-bottom: 2px solid #aaaaaa;
    text-align: center;
    z-index: 0;
}

/* .card_Head {
    width: 375px;
    height: 30px;
    margin-bottom: -4px;
    border-bottom: 2px solid #000000;
} */

.card_Info {
    display: flex;
}

.card_Link {
    display: block;
    width: 40px;
    height: 40px;
    margin: 20px;
}

.card_Link img {
    width: 40px;
    height: 40px;
}

.card_Date {
    margin: auto;
    padding-right: 50px;
    font-size: 18px;
}

.card_Image {
    max-width: 100%;
    height: auto;
    /* border-bottom: 1px solid #000; */
    /* margin-top: 20px; */
}

.card_Movie {
    max-width: 100%;
    height: auto;
    /* border: 1px solid #000; */
    /* margin-top: 20px; */
}

.btn-box {
    display: flex;
}

.left-btn {
    width: 75px;
    height: 52px;
    display: block;
    text-decoration-line: none;
    margin-left: auto;
    margin-right: auto;
}

.right-btn {
    width: 75px;
    height: 52px;
    display: block;
    text-decoration-line: none;
    margin-left: auto;
    margin-right: auto;
}

.ac-box {
    width: auto;
    margin: 10px auto;
}

.ac-box input {
    display: none;
}

.card_Text {
    width: 80%;
    /* 省略せずに表示するサイズを指定 */
    height: auto;
    display: -webkit-box;
    overflow: hidden;
    -webkit-line-clamp: 1;
    /* 省略せずに表示する行数を指定 */
    -webkit-box-orient: vertical;
    margin: auto;
}

.card_LinkText {
    display: none;
}

.ac-box label {
    width: 75px;
    height: 52px;
    font-size: 16px;
    text-align: center;
    margin: 15px auto 0;
    line-height: 50px;
    position: relative;
    display: block;
    cursor: pointer;
    background-image: url("../assets/button.png");
    background-repeat: no-repeat;
    background-size: 50px;
    background-position: center;
}

.ac-box label:hover {
    opacity: 0.7;
}

.ac-box input:checked~label {
    background-image: url("../assets/button_Cancel.png");
}

.ac-box input:checked~.card_Text {
    display: block;
    /* displayをblockに変更することで表示制限を解除 */
    text-align: left;
    margin-bottom: 10px;
}

.ac-box input:checked~.card_LinkText {
    display: block;
}

.Hello2 {
    display: inline-block;
    max-width: 100%;
}

.button_More {
    background: #aaaaaa;
    border: 1px solid #aaaaaa;
    border-radius: 5px;
    font-style: normal;
    width: 50px;
    height: 25px;
    display: block;
    font-size: 16px;
    color: #fff;
    text-decoration-line: none;
    padding: 5px 15px;
    margin-top: 25px;
    margin-left: auto;
    margin-right: auto;
}

@media(min-width: 750px) {
    .card_All {
        width: 373px;
        border: 1px solid #aaaaaa;
    }

    .card_Date {
        font-size: 16px;
    }

    .card_Image {
        width: 373px;
    }

    .card_Movie {
        width: 373px;
    }
}
</style>
    
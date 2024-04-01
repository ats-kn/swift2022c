<template>
    <header>
        <div class="header-inner">
            <!-- ロゴ -->
            <img class="header-logoImg" src="./assets/HaCollectLogo.png">

            <!-- 検索バー -->
            <input type="text" v-model="search_text" v-on:keydown.enter="doSearch" class="searchArea" placeholder="キーワード検索">
        </div>
        <div class="header-inner2">
            <div class="header-nav">
                <input type="radio" checked id="change1" name="header-navlist">
                <label for="change1" id="button11">
                    <router-link class="pageChange" id="button12" to="/">ホーム</router-link>
                </label>
                <input type="radio" id="change2" name="header-navlist">
                <label for="change2" id="button21">
                    <router-link class="pageChange" id="button22" to="/eat">食べる</router-link>
                </label>
                <input type="radio" id="change3" name="header-navlist">
                <label for="change3" id="button31">
                    <router-link class="pageChange" id="button32" to="/see">見る</router-link>
                </label>
                <input type="radio" id="change4" name="header-navlist">
                <label for="change4" id="button41">
                    <router-link class="pageChange" id="button42" to="/know">知る</router-link>
                </label>
            </div>
        </div>
    </header>

    <!-- 現在のリンクごとに表示するコンポーネント -->
    <router-view></router-view>

    <!-- スクロールボタンのトップに戻る処理 -->
    <div>
        <transition name="button">
            <button v-show="buttonActive" class="button" @click="scrollTop"></button>
        </transition>
    </div>
</template>



<script>
'use strict'
export default {
    data() {
        return {
            search_text: '',  //実際にsearchResultコンポーネントに渡すもの
            buttonActive: false,//ボタンを非表示にしておく
            scroll: 0
        }
    },
    methods: {
        InitializeData() {
            this.$store.dispatch('InitializeFireData').then( () => {
                this.$store.dispatch('getTopData')
                this.$store.dispatch('getEatData')
                this.$store.dispatch('getSeeData')
                this.$store.dispatch('getKnowData')
            }) 
        },
        doSearch() {
            try{
                // this.$router.push('/searchResult') <-これはただ、リンク変えるだけ
                this.$router.push({ name: 'searchResult', params: { search: this.search_text } }) //<- これはリンク先に検索したのを渡すことができる
                this.$store.dispatch('getSearchData', this.search_text)    //検索結果ページで使うデータ(search_fire_data)をstoreから参照 -> searchResult.vueのcomputedのfire_dataに反映
                this.search_text = '' //検索バーに検索した文字を残さないための処理
            } catch(e) {
                console.log('error')
                //エラーは無視（search_textに何も入力してない時怒られるから書いた）
            }
        },
        deleteText() {
            this.search_text = '' //検索バーに検索した文字を残さないための処理
        },
        // ページのトップに移動する関数
        scrollTop() {
            window.scrollTo({
                top: 0,  //どこに移動するか
                behavior: 'smooth'  //ここでどのように移動するか決める smoothでゆっくり移動する
            });
        },
        // ボタンが現れる関数
        scrollWindow() {
            const top = 100 //topから100pxスクロールしたらボタン登場
            this.scroll = window.scrollY //垂直方向
            if (top <= this.scroll) {
                this.buttonActive = true   //ボタン見えるようになる
            } else {
                this.buttonActive = false  //ボタン見えない
            }
        }
    },
    mounted() {
        window.addEventListener('scroll', this.scrollWindow)   //スクロールすると関数が察知してくれる
        this.InitializeData();
        document.getElementById('button11').addEventListener("click", function (event) {
            document.getElementById('button12').click();
        });
        document.getElementById('button12').addEventListener("click", function (event) {
            document.getElementById('button11').click();
        });
        document.getElementById('button21').addEventListener("click", function (event) {
            document.getElementById('button22').click();
        });
        document.getElementById('button22').addEventListener("click", function (event) {
            document.getElementById('button21').click();
        });
        document.getElementById('button31').addEventListener("click", function (event) {
            document.getElementById('button32').click();
        });
        document.getElementById('button32').addEventListener("click", function (event) {
            document.getElementById('button31').click();
        });
        document.getElementById('button41').addEventListener("click", function (event) {
            document.getElementById('button42').click();
        });
        document.getElementById('button42').addEventListener("click", function (event) {
            document.getElementById('button41').click();
        });
        // document.getElementById('button51').addEventListener("click", function (event) {
        //     document.getElementById('button52').click();
        // });
        // document.getElementById('button52').addEventListener("click", function (event) {
        //     document.getElementById('button51').click();
        // });
    },
}
</script>



<style>
/* PC用スタイル */
header {
    background-color: #ffffff;
    position: fixed;
    /* 要素を画面内で固定する */
    top: 0;
    /* 固定する基準を一番上に */
    left: 0;
    /* 固定する基準を一番左に */
    z-index: 100;
    /* 要素の重なりを指定 */
    width: 100%;
    /* 固定した要素は浮いた状態になるので、横幅100%にする */
    height: 70px;
}
.header-inner {
    display: flex;
    background: #fff;
    height: 70px;
    justify-content: space-between;
    align-items: center;
    padding: 0 5px;
    margin: 0 auto;
}
.header-logoImg {
    display: block;
    /* 扱いやすいようにblock要素にする */
    width: 60px;
    /* 横幅を任意の大きさに調整 */
    margin-top: 10px;
}
.searchArea {
    width: 500px;
    /* inputの幅 */
    height: 35px;
    background-repeat: no-repeat;
    /* 背景は繰り返さない  */
    background-position: 8px center;
    /* 背景の位置          */
    background-size: auto 60%;
    /* 背景のサイズ        */
    background-color: #fff;
    /* 背景色              */
    margin-top: 10px;
    /* サンプルは中央寄せ  */
    margin-left: 10px;
    /* アイコン間の左余白    */
    border-radius: 10px;
    /* 角丸                */
    color: #687684;
    /* 文字色              */
    font-size: 18px;
    /* フォントサイズ      */
    letter-spacing: 0.1em;
    /* 文字間隔            */
    font-weight: bold;
    /* 太字                */
    outline: 0;
    /* 入力薄枠を非表示    */
    border: 1px solid #CCCCCC;
    font-style: normal;
    text-align: center;
}
/*テキスト入力欄にフォーカスか来たとき*/
.searchArea:focus {
    background-color: #e6f2ff;
    /* フォーカス時背景色  */
}
.header-inner2 {
    background-color: #fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin: 0 auto;
    position: fixed;
    height: 45px;
    z-index: 1;
}
.header-nav {
    display: flex;
    overflow-x: scroll;
    white-space: nowrap;
    height: 45px;
    width: 100%;
}
.header-nav label {
    background: #FFF;
    border-left: 1px solid #CCCCCC;
    border-right: 1px solid #CCCCCC;
    border-bottom: 1px solid #bbbbbb;
    font-style: normal;
    width: 25%;
}
.pageChange {
    display: block;
    /* 扱いやすいようにblock要素にする */
    font-size: 16px;
    /* 任意のフォントサイズにする */
    font-weight: bold;
    /* 太字にする */
    color: #808080;
    text-decoration-line: none;
    padding: 10px 15px;
}
.header-nav input:checked+ label {
    background: #FFFFFF;
    border-top: 1px solid #bbbbbb;
    border-left: 1px solid #bbbbbb;
    border-right: 1px solid #bbbbbb;
    border-bottom: none;
}
.header-nav input:checked+ label .pageChange {
    color: #000;
}
.header-nav input {
    display: none;
}
/* ページトップへ自動スクロールするボタンのスタイル */
.button {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    background-color: orange;
    border-radius: 50%;
    background-image: url('data:image/svg+xml, <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="%23ffffff" d="M0 16.67l2.829 2.83 9.175-9.339 9.167 9.339 2.829-2.83-11.996-12.17z"/></svg>');
    background-repeat: no-repeat;
    background-size: 20px;
    background-position: center;
    cursor: pointer;
    opacity: 0.7;
    /* ボタンにカーソルを合わせるとポインターになる */
}
/* アニメーション中のスタイル */
.button-enter-active,
.button-leave-active {
    transition: opacity 0.5s;
    /* 何秒かけて変わるのか */
}
/* 表示するアニメーション */
.button-enter-from {
    opacity: 0;
}
.button-enter-to {
    opacity: 0.7;
}
/* 非表示にするアニメーション */
.button-leave-from {
    opacity: 0.7;
}
.button-leave-to {
    opacity: 0;
}
/* タブレット・スマートフォン用スタイル */
/* @media(max-width: 971px) {
    .header-logoImg {
        width: 150px;
        margin-top: 10px;
    }
    .searchArea {
    width: 225px;
    height: 30px;
    }
} */
/* スマートフォン用スタイル */
@media(min-width: 750px) {
    .header-inner {
        padding: 0 36px;
    }
    /* .searchArea {
        width: 225px;
        height: 30px;
    } */
    /* .header-inner {
        display: block;
        height: 35px;
    }
    .header-logoImg {
        margin: 0 auto;
    }
    .searchArea {
        display: none;
    } */
}
</style>
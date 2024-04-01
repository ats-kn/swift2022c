import { createStore } from 'vuex'
import createPersistedState from "vuex-persistedstate"
import { initializeApp } from "firebase/app";
import { getDatabase, ref, get, query, orderByChild} from "firebase/database";
// ↑ realtime databaseが必要だったためインポートした {}の中に欲しい機能をかく
//このコードではgetDatabase(realtime Database) と ref, getなどの機能をインポートしている


// Firebaseの設定  (.envファイル作ってそこに自分のFIrebaseのAPI key貼ってください)
const firebaseConfig = {
    apiKey: import.meta.env.VITE_APP_FIREBASE_APIKEY,
    authDomain: import.meta.env.VITE_APP_FIREBASE_AUTH_DOMAIN,
    projectId: import.meta.env.VITE_APP_FIREBASE_PROJECT_ID,
    storageBucket: import.meta.env.VITE_APP_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: import.meta.env.VITE_APP_FIREBASE_MESSAGING_SENDER_ID,
    appId: import.meta.env.VITE_APP_FIREBASE_APP_ID,
    databaseURL: import.meta.env.VITE_APP_FIREBASE__DATABASE_URL //DBのURLを追加
};

// Firebaseの初期化（initializeAppで自分のfirebaseに接続してる？）
const app = initializeApp(firebaseConfig);
const database = getDatabase(app)

// 最初にDBからデータを取得してくる際のインスタの除外ワード
const exclusion_list_str = import.meta.env.VITE_APP_EXCLUSION_LIST;
const exclusion_list = new RegExp(exclusion_list_str);

//カテゴリに表示する時の一致ワード
//食べるカテゴリ
const eat_category_word_list = /ラーメン|ごはん|ご飯|グルメ|カフェ|居酒屋/;
//見るカテゴリ
const see_category_word_list = /スポット|観光|祭|夜景/;
//知るカテゴリ
const know_category_word_list = /スポット|観光|祭|夜景|ラーメン|ごはん|飯|グルメ|カフェ|居酒屋/;

export const store = createStore({
    state() {  
        return {
            //ここにコンポーネント間で共有するデータを書く
            posts_num: 30,                //vueで表示する投稿数
            get_posts_num: 100,        //vue側がDBから取得してくる投稿数
            fire_data: null,                    //全部のカテゴリ＋「函館」で一致するデータを格納する変数
            search_fire_data: null,         //検索結果ページに表示するデータ
            top_fire_data: null,              //トップページに表示するデータ
            eat_fire_data: null,            //食べるカテゴリページに表示するデータ    
            see_fire_data: null,           //見るカテゴリページに表示するデータ
            know_fire_data: null   //知るカテゴリページに表示するデータ
        }
    },
    mutations: {
        //ここにデータを格納する処理"のみ"だけの関数？を書く(mutation->意味：変化)
        setFireData: (state, data) => {         //とりあえず、大枠で、新しいデータを格納する処理
            state.fire_data = data
        },
        setSearchData: (state, data) => {     //検索結果ページに表示するデータに新しいデータを格納する処理
            state.search_fire_data = data
        },
        setTopData: (state, data) => {          //トップページに表示するデータに新しいデータを格納する処理
            state.top_fire_data = data
        },
        setEatData: (state, data) => {        //食べるカテゴリページに表示するデータに新しいデータを格納する処理
            state.eat_fire_data = data
        },
        setSeeData: (state, data) => {        //見るカテゴリページに表示するデータに新しいデータを格納する処理
            state.see_fire_data = data
        },
        setKnowData: (state, data) => {    //知るカテゴリページに表示するデータに新しいデータを格納する処理
            state.know_fire_data = data
        }
    },
    actions: {
        //ここにmutationsを実行するための関数を書く。そして、actionsをvue側で呼び出す。
        InitializeFireData: (context) => {                         //まず、おおもとのデータを取得する処理      
            
            return new Promise(function(resolve, reject) {
                try {
                    const que = query(ref(database, 'SNS_data/'), orderByChild('date'));  //SNS_dataを投稿日を秒数にしてマイナスをつけ、昇順でソートしたものをqueに格納する
                    let roop_count = 0       //ループ回数

                    get(que).then((snapshot) => {   //snapshot->データ全体  childSnapshot->データ一つ
        
                        const data = [];   //あとでデータの挿入(下のcontext.commit)に使う用
                        snapshot.forEach((childSnapshot) => {
                            if (roop_count < 100) {   //roopcountでループ回数を指定（現在100回ループ=データを全体で100個格納）
                                if (childSnapshot.val().SNS_type == 'Instagram') {
                                    let result = exclusion_list.test(childSnapshot.val().text)   //投稿テキストに除外ワードが入っているかチェック
                                    if (result == false) {
                                        // ↓変数dataに、除外ワードが含まれていない、データベースのデータ一つを格納する処理                                    
                                        data.push(childSnapshot.val());
                                    }                                    
                                } else {
                                    // ↓変数dataにデータベースのデータ一つを格納する処理                                    
                                    data.push(childSnapshot.val());
                                }
                                // console.log(roop_count)  //確認用
                                roop_count ++
                            }
                        });
        
                        console.log(data);  //確認用
                        context.commit('setFireData', data)
                        return resolve('Sucsess!')
                    });                     
                } catch(e) {
                    reject('Failed!')
                }
            })
        },
        getSearchData: (context, search) => {           //検索結果ページに表示するデータをRealtime databaseから取得してくる処理
            
            const data = [];
            // fdataにstateに書かれてあるtop_fire_dataを参照する
            //(参照する時点でtop_fire_dataにrealtime databaseのデータが入ってないといけない →getTopDataが前に実行されるべき -> topPage.vueで実行してます）
            const fdata = context.state.fire_data       
        
            for (let i = 0; fdata[i] != null; i++) {
                //includes関数によって、resultには大文字と小文字は区別し、値が見つからない場合はfalseを返します。
                let result = fdata[i].text.includes(search);   //投稿テキストにsearch変数の値が含まれているかどうかをチェック
                // console.log(result)  //確認用
                if(result == true) {
                    data.push(fdata[i]);
                }
            }

            // console.log(data) //確認用
            context.commit('setSearchData', data)     //emutationsのsetSearchDataを実行する
        },
        getTopData: (context) => {                           //トップページに表示するデータをRealtime databaseから取得してくる処理
            
            console.log(context.state.fire_data) //確認用
            context.commit('setTopData', context.state.fire_data)     //emutationsのsetSearchDataを実行する
        },
        getEatData: (context) => {                         //食べるカテゴリページに表示するデータをRealtime databaseから取得してくる処理
                        
            const data = [];
            const fdata = context.state.fire_data
            
            for (let i = 0; fdata[i] != null; i++) {
                if (fdata[i].data_label == 'EatTimeLine'){
                    data.push(fdata[i]);
                } else if(fdata[i].data_label == 'Search') {
                    //testもincludesと役割はほぼ同じ（正規表現が使えるかどうかの違い）
                    let result = eat_category_word_list.test(fdata[i].text);   //投稿テキストにeat_category_word_listの値が一つでも含まれているかどうかをチェック
                    // console.log(result)  //確認用
                    if(result == true) {
                        data.push(fdata[i]);
                    }                    
                }
            }       
            
            console.log(data) //確認用
            context.commit('setEatData', data)
        },
        getSeeData: (context) => {                          //見るカテゴリページに表示するデータをRealtime databaseから取得してくる処理
                        
            const data = [];
            const fdata = context.state.fire_data
            for (let i = 0; fdata[i] != null; i++) {
                if (fdata[i].data_label == 'SeeTimeLine'){
                    data.push(fdata[i]);
                } else if(fdata[i].data_label == 'Search') {
                    let result = see_category_word_list.test(fdata[i].text);
                    //console.log(result)  //確認用
                    if(result == true) {
                        data.push(fdata[i]);
                    }                    
                }
            }   
            
            console.log(data) //確認用
            context.commit('setSeeData', data)
        },
        getKnowData: (context) => {                          //知るカテゴリページに表示するデータをRealtime databaseから取得してくる処理
                        
            const data = [];
            const fdata = context.state.fire_data
            for (let i = 0; fdata[i] != null; i++) {
                if (fdata[i].data_label == 'KnowTimeLine'){
                    data.push(fdata[i]);
                } else if(fdata[i].data_label == 'Search') {                    
                    let result = know_category_word_list.test(fdata[i].text);
                    //console.log(result)  //確認用
                    if(result == false) {
                        data.push(fdata[i]);
                    }                    
                }
            }
            
            console.log(data) //確認用
            context.commit('setKnowData', data)
        },        
    },     
    plugins: [
        createPersistedState()
    ]
})


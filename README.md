# chainsaw-man-box-office-revenue

**Chainsaw Man: Reze Arc Box Office Revenue Graph and Forecast**
**「劇場版 チェンソーマン　レゼ篇」の興行収入と勝手な予測。**
「劇場版「鬼滅の刃」無限城編 第一章 猗窩座再来」の興行収入グラフも収容。

12月、落ち込みが見えるが、100億円越えニュースの効果もあるのか、1月からブーストがかかっており、早ければ2末107億円が見える。少なくとも上映終了までに106億達成は確実か。

ただ、ロングラン枠なので3末まで引っ張る劇場もありそう。さらに、記録狙いで半ば強引にGW開けまで引っ張れば109億もあるのか、というところ。「鬼滅の刃　猗窩座再来」がまだ頑張っており、お互いに影響があると思われる。ズートピア２の場合、客層の重なりは大きくないと見られるが、スクリーンの奪い合いという意味では影響がある。

## データソース

興行収入データは以下のサイトを参考にした。

- [『チェンソーマン レゼ篇』最新興収発表！歴代興収ランキングは47位](https://www.sanyonews.jp/article/1870981?kw=%E3%83%81%E3%82%A7%E3%83%B3%E3%82%BD%E3%83%BC%E3%83%9E%E3%83%B3)

- [『鬼滅の刃』興収393.2億円突破　公開から200日以上…まだ特典配布中！記録更新まで残り14.3億円](https://www.sanyonews.jp/article/1870980?kw=%E7%8C%97%E7%AA%A9%E5%BA%A7%E5%86%8D%E6%9D%A5)

- [映画興行収入データベース](https://www.kogyotsushin.com/archives/alltime/)

## 動作環境準備

Python 3.9.11などでも動くが、3.12.10を推奨。
pyenv、poetryがインストールされており、pyenvによるPython 3.12.10がインストールされている場合、以下のワンラインで。

```bash
poetry install
```

Python 3.12.10のインストールができない場合は、pyenvの再インストールをおすすめする。pyenv-winのバージョンが古くなっているなどでpyenv updateなどがうまく動かない場合がある。

## コードの動かし方

plot.ipynbを開き、カーネルを仮想環境のPython 3.12.10に設定して実行すれば、グラフが生成される。plot.pyにも同様のコードを収容している。

## Python環境の指定

VS Codeでは以下の3つについて自由にPython環境を指定できるが、プロジェクト内の「.venv（仮想環境）」に統一しておくと勘違いが少ない。

- VS Code自体　右下の「インタープリター選択」あるいは、Pythonバージョン表示をクリックして選択。plot.pyを編集ペインで開いておくこと。

- ターミナル（ペイン）　新しいターミナルを追加で開くと、自動的に仮想環境がアクティベートされる。

- Jupyter Notebook　右上のカーネル選択で指定

[<img src="./chainsaw-man-box-office-revenue-forecast.png" width="600">](./chainsaw-man-box-office-revenue-forecast.png)

## 日本語フォントに関して
日本語フォントがうまく設定できていなかったりキャッシュが更新されていないと文字化け（豆腐化）が発生する。

### フォントの指定方法

matplotlibのフォント指定は以下のようにフォントファミリー名でおこなう。

```python
plt.rcParams['font.family'] = 'Yu Gothic UI'
```

指定に使うフォントファミリー名を得るには、plot.ipynbに収容してある、以下のコードでリストを取得して確認する。

```python
import matplotlib.font_manager as fm

font_names=[]
for font_path in fm.findSystemFonts():
    try:
        font_name = fm.FontProperties(fname=font_path).get_name()
    except Exception as e:
        print(font_path)
        print("ERROR::: can't get the font name from the file above.  ", e)
        print("********")
    finally:
        font_names.append(font_name)

    font_names2 = list(set(font_names))
    font_names2.sort()

for font_name in font_names2:
    print(font_name)
```

### キャッシュ問題
matplotlibが持つキャッシュのクリアが必要な場合は、以下のコードで。新しいフォントをインストールした場合は、キャッシュのクリアが必須。これもplot.ipynbに収容してある。

```python
import shutil
import matplotlib

shutil.rmtree(matplotlib.get_cachedir())
```

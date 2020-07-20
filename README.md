# DiceChan

## /d100
1から100までの整数を一つ出す。一様分布。
- option:<br>
引数に```比較演算子```を用いることで指定した```値```と比較できる。<br>また演算子は組み合わせることができる。<br>組み合わせた時,大なりと小なりが混在されている場合は小なりが優先される。

    - イコール<br>
        'e', 'E', '='が使える。

    - 大なり<br>
        'g', 'G', '>'が使える。

    - 小なり<br>
        'l', 'L', '<'が使える。

```
/d100 演算子 数字

(例)
/d100 <= 10
/d100 g85
/d100 e36
```

## /d20
1から20までの整数を一つ出す。一様分布。
optionは```/d100```と同じ。

## /d *n*d*m*
*m*面ダイスを*n*回降る作用をする。合計値と各値を出力する。optionはない。

## その他
```@ダイスちゃん 使い方```で簡単な説明を出力する。<br>
今後機能を増やしていきます。
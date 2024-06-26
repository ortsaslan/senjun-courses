# Глава 12. Лямбда-функция

Пришло время познакомиться с важной концепцией — лямбда-функцией. Именно с неё всё и началось. Приготовьтесь: в этой главе нас ждут новые открытия.

## Истоки

В далёких 1930-х молодой американский математик [Алонзо Чёрч](https://en.wikipedia.org/wiki/Alonzo_Church) задался вопросом о том, что значит «вычислить» что-либо. Плодом его размышлений явилась система для формализации понятия «вычисление», и назвал он эту систему «лямбда-исчислением» (англ. lambda calculus, по имени греческой буквы `λ`). В основе этой системы лежит лямбда-функция, которую в некотором смысле можно считать «матерью функционального программирования» в целом и Haskell в частности. Далее буду называть её ЛФ.

В отношении ЛФ можно смело сказать: «Всё гениальное просто». Идея ЛФ столь полезна именно потому, что она предельно проста. ЛФ — это анонимная функция. Вот как она выглядит в Haskell:

```haskell
\x -> x * x
```

Обратный слэш в начале — признак ЛФ. Сравните с математической формой записи:

```
λx . x * x
```

Похоже, не правда ли? Воспринимайте обратный слэш в определении ЛФ как спинку буквы `λ`.

ЛФ представляет собой простейший вид функции, эдакая функция, раздетая догола. У неё забрали не только объявление, но и имя, оставив лишь необходимый минимум в виде имён аргументов и внутреннего выражения. Алонзо Чёрч понял: чтобы применить функцию, вовсе необязательно её именовать. 

И если у обычной функции сначала идёт объявление/определение, а затем (где-то) применение с использованием имени, то у ЛФ всё куда проще: мы её определяем и тут же применяем, на месте. Помните функцию `square`? Вот это её лямбда-аналог. В скобках идет лямбда-абстракция, затем 5 — аргумент, с которым она вызывается:

```haskell
(\x -> x * x)  5
```

Лямбда-абстракция (англ. lambda abstraction) — это особое выражение, порождающее функцию, которую мы сразу же применяем к аргументу `5`. ЛФ с одним аргументом, как и простую функцию, называют ещё «ЛФ от одного аргумента» или «ЛФ одного аргумента». Так же можно сказать и о «лямбда-абстракции от одного аргумента».

## Строение

Строение лямбда-абстракции предельно простое: `\` — признак ЛФ, `x` — имя аргумента, `x * x` — выражение.

```haskell
\ x -> x * x
```

Соответственно, если ЛФ применяется к двум аргументам — пишем так:

```haskell
\ x y -> x * y
```

И когда мы применяем такую функцию:

```haskell
(\x y -> x * y) 10 4
```

то просто подставляем `10` на место `x`, а `4` — на место `y`, и получаем выражение `10 * 4`, то есть `40`:

```haskell
(\x y -> x * y) 10 4
```

В общем, всё как с обычной функцией, даже проще.

Мы можем ввести промежуточное значение для лямбда-абстракции:

```haskell {.example_for_playground}
main :: IO ()
main = print (mul 10 4)
  where mul = \x y -> x * y
```

Теперь мы можем применять `mul` так же, как если бы это была сама лямбда-абстракция:

```haskell
  mul 10 4
= (\x y -> x * y) 10 4
= 10 * 4
```

Напишите функцию `area`, которая принимает название фигуры и длину ее грани. Варианты фигур: `"square"` (квадрат), `"triangle"` (прямоугольный треугольник), `"cube"` (куб). {.task_text}

В зависимости от фигуры и значения длины грани функция должна посчитать площадь фигуры. {.task_text}

В теле функции внутри `where` заведите три ЛФ: {.task_text}
- ЛФ для подсчета площади квадрата; 
- использующая ее ЛФ для подсчета площади прямоугольного треугольника;
- также использующая первую ЛФ лямбда, подсчитывающая площадь куба.
{.task_text}

Для фигур, не являющихся квадратом, прямоугольным треугольником или кубом, функция должна возвращать 0.

```haskell {.task_source #haskell_chapter_0120_task_0010}
module Main where

-- Your code here

main :: IO ()
main = do
       print (area "square" 3.0)
       print (area "triangle" 3.0)
       print (area "cube" 3.0)
       print (area "cylinder" 3.0)
```
Для множественного выбора можно воспользоваться конструкцией `case-of`. ЛФ для подсчета площади прямоугольного треугольника может выглядеть так: `triangleArea = \x -> (squareArea x) / 2.0`. Она использует ЛФ `squareArea`. {.task_hint}
```haskell {.task_answer}
module Main where

area :: String -> Double -> Double
area figure side = 
  case figure of
    "square" -> squareArea side
    "triangle" -> triangleArea side
    "cube" -> cubeArea side
    _ -> 0.0
  where
    squareArea = \x-> x*x
    triangleArea = \x -> (squareArea x) / 2.0
    cubeArea = \x -> (squareArea x) * 6
  

main :: IO ()
main = do
       print (area "square" 3.0)
       print (area "triangle" 3.0)
       print (area "cube" 3.0)
       print (area "cylinder" 3.0)
```

И здесь мы приблизились к одному важному открытию.

## Тип функции

Мы знаем, что у всех данных в Haskell-программе обязательно есть какой-то тип, внимательно проверяемый на этапе компиляции. Вопрос: какой тип у выражения `mul` из предыдущего примера?

```haskell
where mul = \x y -> x * y  -- Какой тип?
```

Ответ прост: тип `mul` такой же, как и у этой лямбда-абстракции. Из этого мы делаем важный вывод: ЛФ имеет тип, как и обычные данные. Но поскольку ЛФ является частным случаем функции — значит и у обыкновенной функции тоже есть тип!

В нефункциональных языках между функциями и данными проведена чёткая граница: вот это функции, а вон то — данные. Однако в Haskell между данными и функциями разницы нет, ведь и то и другое покоится на одной и той же Черепахе. Вот тип функции `mul`:

```haskell
mul :: a -> a -> a
```

Погодите, скажете вы, но ведь это же объявление функции! Совершенно верно: объявление функции — это и есть указание её типа. Помните, когда мы впервые познакомились с функцией, я уточнил, что её объявление разделено двойным двоеточием? Так вот это двойное двоеточие и представляет собой указание типа:

```
mul  ::     a -> a -> a

вот  имеет  │   вот   │
это  тип    └─ такой ─┘
```

Что это за буква `a`? Во-первых, мы не встречали такой тип ранее, а во-вторых, разве имя типа в Haskell не обязано начинаться с большой буквы? Обязано. А всё дело в том, что буква `a` в данном случае — это не совсем имя типа. А вот что это такое, мы узнаем в [одной из ближайших глав.](/courses/haskell/chapters/haskell_chapter_0140#block-polymorphic-types) {#block-mul-declaration}

Точно так же мы можем указать тип любых других данных:

```haskell
let coeff = 12 :: Double
```

Хотя мы знаем, что в Haskell типы выводятся автоматически, иногда мы хотим взять эту заботу на себя. В данном случае мы явно говорим: «Пусть выражение `coeff` будет равно `12`, но тип его пусть будет `Double`, а не `Int`». Так же и с функцией: когда мы объявляем её — мы тем самым указываем её тип.

Но вы спросите, можем ли мы не указывать тип функции явно? Можем:

```haskell
square x = x * x
```

Это наша старая знакомая, функция `square`. Когда она будет применена к значению типа `Int`, тип аргумента будет выведен автоматически как `Int`.

И раз функция характеризуется типом так же, как и прочие данные, мы делаем ещё одно важное открытие: функциями можно оперировать как данными. Например, можно создать список функций:

```haskell {.example_for_playground}
main :: IO ()
main = putStrLn ((head functions) "Hi")
  where
    functions = [ \x -> x ++ " val1"
                , \x -> x ++ " val2"
                ]
```

Выражение `functions` — это список из двух функций. Два лямбда-выражения порождают эти две функции, но до момента применения они ничего не делают, они безжизненны и бесполезны. Но когда мы применяем функцию `head` к этому списку, мы получаем первый элемент списка, то есть первую функцию. И получив, тут же применяем эту функцию к строке `"Hi"`:

```
putStrLn ((head functions)  "Hi")

          │    первая    │  её
          │   функция    │  аргумент
          └─ из списка ──┘
```

Это равносильно коду:

```haskell
putStrLn ((\x -> x ++ " val1") "Hi")
```

При запуске программы мы получим:

```
Hi val1
```

Кстати, а каков тип списка `functions`? Его тип таков: `[String -> String]`. То есть список функций с одним аргументом типа `String`, возвращающих значение типа `String`.

## Локальные функции

Итак, между ЛФ и простыми функциями фактически нет различий, а функции есть частный случай данных. Следовательно, мы можем создавать функции локально для других функций:

```haskell {.example_for_playground}
-- Здесь определены функции
-- isInfixOf и isSuffixOf.
import Data.List (isInfixOf, isSuffixOf)

validComEmail :: String -> Bool
validComEmail email =
    containsAtSign email && endsWithCom email
  where
    containsAtSign e = "@" `isInfixOf` e
    endsWithCom e = ".com" `isSuffixOf` e

main :: IO ()
main = putStrLn (if validComEmail my
                   then "It's ok!"
                   else "Non-com email!")
  where
    my = "haskeller@gmail.com"
```

Несколько наивная функция `validComEmail` проверяет `.com`-адрес. Её выражение образовано оператором `&&` и двумя выражениями типа `Bool`. Вот как образованы эти выражения:

```haskell
containsAtSign e = "@" `isInfixOf` e
endsWithCom e = ".com" `isSuffixOf` e
```

Это — две функции, которые мы определили прямо в `where`-секции, поэтому они существуют только для основного выражения функции `validComEmail`. С простыми функциями так поступают очень часто: где она нужна, там её и определяют. Мы могли бы написать и более явно:

```haskell
validComEmail :: String -> Bool
validComEmail email =
    containsAtSign email && endsWithCom email
  where
    -- Объявляем локальную функцию явно.
    containsAtSign :: String -> Bool
    containsAtSign e = "@" `isInfixOf` e

    -- И эту тоже.
    endsWithCom :: String -> Bool
    endsWithCom e = ".com" `isSuffixOf` e
```

Впрочем, указывать тип столь простых функций, как правило, нет необходимости.

Вот как этот код выглядит с лямбда-абстракциями:

```haskell
validComEmail :: String -> Bool
validComEmail email =
    containsAtSign email && endsWithCom email
  where
    containsAtSign = \e -> "@" `isInfixOf` e
    endsWithCom = \e -> ".com" `isSuffixOf` e
```

Теперь выражения `containsAtSign` и `endsWithCom` приравнены к ЛФ от одного аргумента. В этом случае мы не указываем тип этих выражений. Впрочем, если очень хочется, можно и указать:

```haskell
containsAtSign =
    (\e -> "@" `isInfixOf` e) :: String -> Bool
```

Лямбда-абстракция взята в скобки, чтобы указание типа относилось к функции в целом, а не только к аргументу `e`.

Замените функцию `showVal` на ЛФ в блоке `let` функции `main`. Укажите для этой ЛФ тип. {.task_text}

```haskell {.task_source #haskell_chapter_0120_task_0020}
module Main where

showVal :: Int -> String
showVal x = "x = " ++ (show x)

main :: IO ()
main =  do
        putStrLn (showVal 120)
        putStrLn (showVal 50)
        putStrLn (showVal 84)
```
Для указания типа ЛФ не забудьте саму ЛФ взять в скобки. {.task_hint}
```haskell {.task_answer}
module Main where

main :: IO ()
main =  let
        showVal = (\x -> "x = " ++ (show x)) :: Int -> String
        in
          do
          putStrLn (showVal 120)
          putStrLn (showVal 50)
          putStrLn (showVal 84)
```

Для типа функции тоже можно ввести псевдоним!

Импортируйте функции `isInfixOf` и `isSuffixOf` из модуля `Data.List`. {.task_text}

Внутри лямбда-абстракций замените их применение с префиксной на [инфиксную форму.](/courses/haskell/chapters/haskell_chapter_0080#block-infix) {.task_text}

Создайте псевдоним `Func` и с его помощью укажите тип для `validComEmail` и двух лямбда-абстракций. {.task_text}

```haskell {.task_source #haskell_chapter_0120_task_0030}
module Main where

-- Your code here

validComEmail -- And here
validComEmail email =
    containsAtSign email && endsWithCom email
  where
    containsAtSign = (\e -> isInfixOf "@" e) -- And here
    endsWithCom = (\e -> isSuffixOf ".com" e) -- And here

main :: IO ()
main = do
       print (validComEmail "haskeller@gmail.com")
       print (validComEmail "haskellergmail.com")
       print (validComEmail "haskeller@gmailcom")
```
Не забудьте импортировать модуль `Data.List`. Синтаксис объявления псевдонима для типа функции: `type SomeFunc = Bool -> Bool -> Int`. Для инфиксного применения функции ее имя обрамляется обратными одинарными кавычками (англ. backtick). {.task_hint}
```haskell {.task_answer}
module Main where

import Data.List (isInfixOf, isSuffixOf)

type Func = String -> Bool

validComEmail :: String -> Bool
validComEmail email =
    containsAtSign email && endsWithCom email
  where
    containsAtSign = (\e -> "@" `isInfixOf` e) :: Func
    endsWithCom = (\e -> ".com" `isSuffixOf` e) :: Func

main :: IO ()
main = do
       print (validComEmail "haskeller@gmail.com")
       print (validComEmail "haskellergmail.com")
       print (validComEmail "haskeller@gmailcom")
```

Впрочем, на практике указание типа для лямбда-абстракций встречается исключительно редко, ибо незачем.

Отныне, познакомившись с ЛФ, мы будем использовать их периодически.

## Для любопытных

А почему, собственно, лямбда? Почему Чёрч выбрал именно эту греческую букву? По одной из версий, произошло это чисто случайно.

Шли 30-е годы прошлого века, компьютеров не было, и все научные работы набирались на печатных машинках. В первоначальном варианте, дабы выделять имя аргумента ЛФ, Чёрч ставил над именем аргумента символ, похожий на `^`. Но когда он сдавал работу наборщику, то вспомнил, что печатная машинка не сможет воспроизвести такой символ над буквой. Тогда он вынес эту «крышу» перед именем аргумента, и получилось что-то наподобие:

```
^x . x * 10
```

А наборщик, увидев такой символ, использовал заглавную греческую букву `Λ`:

```
Λx . x * 10
```

Вот так и получилось, лямбда-исчисление.

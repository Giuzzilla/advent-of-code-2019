import scala.io.Source

object Day2 {
  
  def firstStar(passedArr: Array[Int], newpos1: Int, newpos2: Int): Int = {
    var arr: Array[Int] = passedArr.clone
    arr(1) = newpos1
    arr(2) = newpos2
    var pos = 0
    while (arr(pos) != 99) {
      arr(pos) match {
        case 1 => arr(arr(pos+3)) = arr(arr(pos+1)) + arr(arr(pos+2))
        case 2 => arr(arr(pos+3)) = arr(arr(pos+1)) * arr(arr(pos+2))
        case default => throw new Exception("Matched " + default)
      }
      pos += 4
    }
    arr(0)
  }

  def secondStar(arr: Array[Int], required: Int): Array[Int] = {
    var matched: Array[Int] = Array()
    for (i <- 0 to 98; j <- 0 to 98) {
      if (firstStar(arr, i, j) == required)
        matched :+= i*100 + j
    }
    matched
  }

  def main(args: Array[String]) {
    if (args.length < 3) {
      throw new Exception("Missing params")  
    }

    val newpos1: Int = args(0).toInt
    val newpos2: Int = args(1).toInt
    val required: Int = args(2).toInt
    
    val path: String = {
      if (args.length == 3)
        "./input.txt"
      else
        args(4)
    }


    val arr: Array[Int] = Source.fromFile(path).getLines.toList(0).split(",").map(_.toInt)
    println("First answer: " + firstStar(arr, newpos1, newpos2))
    val matched: Array[Int] = secondStar(arr, required)
    if (matched.length > 0)
      println("Second answer: " + matched(0))
  }
}

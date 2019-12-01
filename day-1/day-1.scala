import scala.io.Source
import scala.annotation.tailrec

object Day1 {
  @tailrec def secondStar(fuel: Int, aggr: Int = 0) : Int = {
    val current_fuel : Int = fuel / 3 - 2
    if (current_fuel <= 0)
      aggr
    else
      secondStar(current_fuel, aggr + current_fuel)
  }

  def main(args: Array[String]) {
    val path : String = {
      if (args.length == 0) 
        "./input.txt"
      else
        args(0)
    }

    val list = Source.fromFile(path).getLines.toArray.map(_.toInt)
    println("First answer: " + list.map(x => x / 3 - 2).sum)
    println("Second answer: " + list.map(x => secondStar(x)).sum)

  }
}

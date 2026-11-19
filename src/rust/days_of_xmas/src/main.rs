const ORDINALS: [&str; 12] = [
    "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth",
    "eleventh", "twelth",
];

fn main() {
    for i in 1..13 {
        println!(
            "On the {} day of Christmas my true love sent to me",
            ORDINALS[i - 1]
        );
        if i >= 12 {
            println!("Twelve drummers drumming")
        }
        if i >= 11 {
            println!("Eleven pipers piping")
        }
        if i >= 10 {
            println!("Ten lords a-leaping")
        }
        if i >= 9 {
            println!("Nine ladies dancing")
        }
        if i >= 8 {
            println!("Eight maids a-milking")
        }
        if i >= 7 {
            println!("Seven swans a-swimming")
        }
        if i >= 6 {
            println!("Six geese a-laying")
        }
        if i >= 5 {
            println!("Five golden rings")
        }
        if i >= 4 {
            println!("Four calling birds")
        }
        if i >= 3 {
            println!("Three French hens")
        }
        if i >= 2 {
            println!("Two turtle doves")
        }
        if i == 1 {
            println!("A partridge in a pear tree")
        } else {
            println!("And a partridge in a pear tree")
        }
    }
}

use std::fs::read_to_string;
use std::collections::HashMap;
use std::fmt;
use std::cmp::{min,max};

const MAP_SIZE: usize = 20;
const INPUT_FILE: &str = "test_input";

#[derive(Debug)]
struct Coordinate {
    x: usize,
    y : usize,
}

fn area(a : &Coordinate, b : &Coordinate) -> usize {
    return (((a.x as i64 - b.x as i64).abs() + 1) * ((a.y as i64 - b.y as i64).abs() + 1)) as usize
}

fn biggest_rect(coords: &Vec<Coordinate>) -> usize {
    let mut largest_area: usize = 0;

    for a in coords {
        for b in coords {
            let cur = area(a,b);
            if cur > largest_area {
                largest_area = cur;
            }
        }
    }

    return largest_area;
}

#[derive(Copy,Clone,Debug,PartialEq)]
enum Tile {
    Red,
    Green,
    Exterior,
    Unknown,
}

struct Theater {
    map: Vec<Vec<Tile>>,
}

impl fmt::Display for Theater {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for row in &self.map {
            for tile in row {
                write!(f, "{}", match tile {
                    Tile::Red => "#",
                    Tile::Green => "X",
                    Tile::Unknown => " ",
                    Tile::Exterior => ".",
                })?;
            }
            write!(f, "\n")?;
        }
        Ok(())
    }
}

fn boundary(coords: &Vec<Coordinate>) -> Theater {
    let mut map: Vec<Vec<Tile>> = Vec::new();
    for i in 0..MAP_SIZE {
        let mut row: Vec<Tile> = Vec::new();
        for j in 0..MAP_SIZE {
            row.push(Tile::Unknown);
        }
        map.push(row);
    }

    let mut t = Theater {
        map: map,
    };

    let mut prev = &coords[0];
    t.map[prev.x][prev.y] = Tile::Red;
    for a in &coords[1..] {
        if prev.x == a.x {
            for y in min(prev.y,a.y) .. max(prev.y,a.y)+1 {
                t.map[prev.x][y] = Tile::Green;
            }
        } else if prev.y == a.y {
            for x in min(prev.x,a.x) .. max(prev.x,a.x)+1 {
                t.map[x][prev.y] = Tile::Green;
            }
        } else{
            panic!("foo");
        }
        t.map[prev.x][prev.y] = Tile::Red;
        t.map[a.x][a.y] = Tile::Red;
        prev = a;
    }
    let a = &coords[0];
    if prev.x == a.x {
        for y in min(prev.y,a.y) .. max(prev.y,a.y)+1 {
            t.map[prev.x][y] = Tile::Green;
        }
    } else if prev.y == a.y {
        for x in min(prev.x,a.x) .. max(prev.x,a.x)+1 {
            t.map[x][prev.y] = Tile::Green;
        }
    } else{
        panic!("foo");
    }
    t.map[prev.x][prev.y] = Tile::Red;
    t.map[a.x][a.y] = Tile::Red;


    return t
}

fn fill(theater: &mut Theater) {
    let mut s: Vec<(usize,usize)> = Vec::new();
    s.push((0,0));

    while s.len() > 0 {
        let p = s.pop().unwrap();
        let mut x = p.0;
        let y = p.1;

        let mut lx = x;
        while lx >= 1 && theater.map[lx-1][y] == Tile::Unknown {
            theater.map[lx-1][y] = Tile::Exterior;
            lx -= 1;
        }

        while x < theater.map.len() && theater.map[x][y] == Tile::Unknown {
            theater.map[x][y] = Tile::Exterior;
            x += 1;
        }

        if x >= 1 {
            scan(&theater,lx, x-1, y+1, &mut s);
        }
        if x >= 1 && y >= 1 {
            scan(&theater,lx, x-1, y-1, &mut s);
        }
    }
}

fn scan(t : &Theater, lx: usize, rx: usize, y: usize, s : &mut Vec<(usize,usize)>) {
    if y >= t.map[0].len() {
        return;
    }

    let mut span_added = false;
    for x in lx .. rx+1 {
        if x >= t.map.len() {
            continue;
        }
        if t.map[x][y] != Tile::Unknown {
            span_added = false;
        } else if !span_added {
            s.push((x,y));
            span_added = true;
        }
    }
}

fn largest_rect_inside(t: &Theater, coords: &Vec<Coordinate>) -> usize {
    let mut largest_area: usize = 0;

    for a in coords {
        for b in coords {
            let cur = area(a,b);

            if cur > largest_area {
                // suffices to only check border of the rectangle
                let min_x = min(a.x, b.x);
                let max_x = max(a.x,b.x);
                let min_y = min(a.y,b.y);
                let max_y = max(a.y,b.y);

                // optimization: check extrema first

                if t.map[min_x][min_y] == Tile::Exterior {
                    continue
                }

                if t.map[min_x][max_y] == Tile::Exterior {
                    continue
                }

                if t.map[max_x][min_y] == Tile::Exterior {
                    continue
                }

                if t.map[max_x][max_y] == Tile::Exterior {
                    continue
                }

                let mut ok = true;

                for x in min_x .. max_x+1 {
                    match t.map[x][min_y] {
                        Tile::Exterior => {
                            ok=false;
                            break;
                        },
                        _ => (),
                    }
                    match t.map[x][max_y] {
                        Tile::Exterior => {
                            ok=false;
                            break;
                        },
                        _ => (),
                    }
                }
                for y in min_y .. max_y+1 {
                    match t.map[min_x][y] {
                        Tile::Exterior => {
                            ok=false;
                            break;
                        },
                        _ => (),
                    }
                    match t.map[max_x][y] {
                        Tile::Exterior => {
                            ok=false;
                            break;
                        },
                        _ => (),
                    }
                }
                if !ok {
                    continue
                }
                println!("{}", cur);
                largest_area = cur;
            }
        }
    }

    return largest_area;
}

fn main() {
    let mut coords: Vec<Coordinate> = Vec::new();

    for line in read_to_string(INPUT_FILE).unwrap().lines() {
        let coord: Vec<&str> = line.split(",").collect();
        coords.push(Coordinate{x: coord[0].parse::<usize>().unwrap_or(0), y: coord[1].parse::<usize>().unwrap_or(0)})
    }

    println!("done loading coords");
    let mut t = boundary(&coords);
    println!("done boundary");
    println!("{}", t);
    fill(&mut t);
    println!("done fill");
    println!("{}", t);
    println!("{:#?}", biggest_rect(&coords));
    println!("done biggest rect");
    println!("{:#?}", largest_rect_inside(&t, &coords));
}

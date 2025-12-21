use std::{collections::HashMap, fs::read_to_string};


struct DAG {
    edges: HashMap<String,Vec<String>>,
}

impl DAG {
    fn new() -> DAG {
        return DAG {
            edges: HashMap::new(),
        };
    }

    fn add_edges(&mut self, a: &str, bs: Vec<&str>) {
        let default: Vec<String> = Vec::new();
        let edges= &mut self.edges.remove(&a.to_string()).unwrap_or(default);

        for b in bs {
            if !edges.contains(&b.to_string()) {
                edges.push(b.to_string());
            }
        }


        self.edges.insert(a.to_string(), edges.to_vec());
    }

    fn paths(&self, memo: &mut HashMap<String,u64>, src: &str, dst: &str) -> u64 {
        if src == dst {
            return 1;
        } else if let Some(edges) = self.edges.get(&src.to_string()) {
            let mut count = 0;

            for out in edges {
                if let Some(res) = memo.get(out) {
                    count += res.clone();
                } else {
                    let res = self.paths(memo, out, dst);
                    memo.insert(out.to_string(), res);
                    count += res;
                }
            }

            return count;
        }
            

        return 0;
    }
}

const INPUT_FILE: &str = "input";

fn main() {
    let mut g = DAG::new();
    for line in read_to_string(INPUT_FILE).unwrap().lines() {
        let parts: Vec<&str> = line.split(":").collect();
        let src = parts[0].trim();
        let dsts: Vec<&str> = parts[1].split(" ").map(|x| x.trim()).collect();
        // println!("{} {}", src, dsts);
        g.add_edges(src, dsts);
    }

    // println!("{}", g.paths(&mut HashMap::new(), "you","out"));

    println!("{}", g.paths(&mut HashMap::new(), "svr","fft") * g.paths(&mut HashMap::new(), "fft","dac") * g.paths(&mut HashMap::new(), "dac","out")
        + g.paths(&mut HashMap::new(), "svr","dac") * g.paths(&mut HashMap::new(), "dac","fft") * g.paths(&mut HashMap::new(), "fft","out"));

}

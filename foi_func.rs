use chrono::Datelike;
use clap::Parser;

/// Calcolo rivalutazione monetaria con indice FOI.
#[derive(Parser)]
struct Cli {
    /// From date "YYYY-MM-DD"
    from: chrono::NaiveDate,
    /// To date "YYYY-MM-DD"
    to: chrono::NaiveDate,
}

fn main() {
    let args = Cli::parse();

    test_riv_foi(args.from.year(), args.from.month(), args.to.year(), args.to.month());
}

/*****
fn test() {
    test_riv_foi(1992, 1, 1992, 2);
    test_riv_foi(1992, 1, 1992, 3);
    test_riv_foi(1992, 1, 1992, 4);
    test_riv_foi(1992, 1, 1992, 5);
    test_riv_foi(1992, 1, 1992, 6);
    test_riv_foi(1992, 1, 1992, 7);
    test_riv_foi(1992, 1, 1992, 8);
    test_riv_foi(1992, 1, 1992, 9);
    test_riv_foi(1992, 1, 1992, 10);
    test_riv_foi(1992, 1, 1992, 11);
    test_riv_foi(1992, 1, 1992, 12);
    test_riv_foi(1992, 1, 1993, 1);
    test_riv_foi(1992, 1, 1992, 2);
    test_riv_foi(1992, 2, 1992, 3);
    test_riv_foi(1947, 1, 2023, 7);
}
*****/

fn test_riv_foi(year1: i32, month1: u32, year2: i32, month2: u32) {
    println!("from {}-{} to {}-{}      riv = {:7.3}", year1, month1, year2, month2, riv_foi(year1, month1, year2, month2));
}

fn riv_foi(year1: i32, month1: u32, year2: i32, month2: u32) -> f32 {
    let y1: i32;
    let y2: i32;
    let m1: u32;
    let m2: u32;
    if (year2 * 100 + (month2 as i32)) > (year1 * 100 + (month1 as i32)) {
        y1 = year1;
        y2 = year2;
        m1 = month1;
        m2 = month2;
    } else {
        y1 = year2;
        y2 = year1;
        m1 = month2;
        m2 = month1;
    }
    
    let crb: [(i32, f32); 10] = [(1966, 1.274), (1970, 1.116), (1976, 1.996), (1980, 1.862), (1985, 1.907), (1989, 1.242), (1992, 1.189), (1995, 1.141), (2010, 1.373), (2015, 1.071)];
    let mut crbv: f32 = 1.0;
    for val in crb {
        if (y1 <= val.0) && (y2 > val.0) {
            crbv = crbv * val.1;
        }
    }

    let cst: f32;
    if ((y1 * 100 + m1 as i32) < 199202) && ((y2 * 100 + m2 as i32) >= 199202) {
        cst = 1.0009;
    } else {
        cst = 1.0;
    }

    if (year2 * 100 + month2 as i32) > (year1 * 100 + month1 as i32) {
        foi_idx(year2, month2) / foi_idx(year1, month1) * crbv * cst
    } else {
        foi_idx(year1, month1) / foi_idx(year2, month2) / crbv / cst
    }

}

fn foi_idx(yyyy: i32, mm: u32) -> f32 {
    // Indice dei prezzi al consumo per le rivalutazioni monetarie
    // indice dei prezzi al consumo per le famiglie di operai e impiegati (FOI)
    // al netto dei tabacchi.
    // Dati Aggiornati fino a SETTEMBRE 2023.
    // Dati pubblicati il 15 OTTOBRE 2023.
    // Prossimo aggiornamento il 15 NOVEMBRE 2023.
    // http://www.istat.it/it/archivio/30440

    let aidx: [[f32; 13]; 77] = [
        [ 51.68, 52.78, 54.29, 59.15, 62.06,  66.1,  68.23,  71.98,  75.7,  75.49,  72.2,   69.99,  64.97],
        [ 68.76, 68.03, 69.85, 70.11, 69.21,  68.66, 65.34,  68.05,  69.72, 68.7,   69.16,  69.82,  68.79],
        [ 70.79, 70.41, 70.72, 71.74, 71.67,  70.86, 68.89,  69.72,  69.38, 67.85,  68.02,  67.5,   69.8],
        [ 67.24, 67.41, 66.49, 67.48, 67.59,  68.49, 68.5,   69.71,  71.1,  70.24,  70.96,  71.13,  68.86],
        [ 72.14, 73.43, 73.83, 75.5,  75.59,  76.6,  76.57,  76.3,   76.27, 76.48,  76.95,  76.91,  75.55],
        [ 76.67, 77.52, 77.75, 78.12, 78.42,  78.94, 79.13,  79.17,  79.74, 79.89,  79.99,  79.69,  78.76],
        [ 79.57, 79.72, 79.71, 80.49, 80.97,  81.2,  79.99,  79.76,  80.12, 80.43,  80.82,  80.63,  80.29],
        [ 80.74, 81.08, 80.84, 81.35, 82.39,  83.07, 83.37,  83.29,  83.17, 83.03,  83.41,  83.53,  82.45],
        [ 83.5,  83.31, 83.5,  84.19, 84.96,  85.53, 85.22,  85.36,  85.1,  85.08,  85.44,  86.01,  84.76],
        [ 86.61, 87.77, 88.81, 89.35, 89.82,  89.45, 89.25,  89.29,  89.53, 89.04,  89.14,  89.62,  88.98],
        [ 90.5,  89.96, 89.52, 89.46, 89.78,  89.96, 90.51,  90.59,  91.01, 91.75,  92.4,   92.93,  90.7],
        [ 93.87, 93.48, 93.61, 95.09, 96.08,  96.73, 96.49,  96.05,  95.74, 94.82,  94.48,  94.01,  95.04],
        [ 94.38, 94.11, 93.85, 94.02, 94.28,  94.26, 94.15,  94.29,  94.75, 95.38,  95.98,  96.28,  94.65],
        [ 97.05, 96.66, 96.31, 96.48, 96.89,  97.27, 97.53,  97.37,  97.29, 97.32,  97.77,  98.03,  97.16],
        [ 98.81, 98.86, 98.92, 99.52, 99.87, 100.03, 99.91, 100.1,  100.4, 100.55, 101.31, 101.78, 100.0],
        [102.7, 102.8, 103.4, 104.7, 104.7, 105.2, 105.6, 105.4, 105.9, 106.3, 106.7, 107.8, 105.1],
        [109.6, 111.6, 112.1, 112.7, 112.7, 112.7, 112.6, 112.8, 113.9, 115.0, 115.0, 115.7, 113.0],
        [116.8, 117.1, 117.6, 118.1, 118.6, 119.7, 120.4, 120.6, 121.1, 121.8, 122.3, 122.8, 119.7],
        [123.4, 123.6, 123.9, 124.2, 124.6, 124.9, 125.3, 125.4, 125.6, 125.7, 125.8, 126.3, 124.9],
        [126.7, 126.7, 126.8, 127.2, 127.5, 127.4, 127.5, 127.4, 127.4, 127.8, 128.2, 128.6, 127.4],
        [101.2, 101.1, 101.3, 101.5, 101.7, 101.9, 102.1, 102.3, 102.7, 102.6, 102.6, 102.6, 102.0],
        [103.0, 102.9, 103.0, 103.2, 103.3, 103.2, 103.1, 103.2, 103.4, 103.5, 103.6, 104.0, 103.3],
        [104.3, 104.3, 104.7, 105.2, 105.4, 105.8, 106.5, 106.8, 107.1, 107.6, 108.0, 108.5, 106.2],
        [109.1, 109.9, 110.2, 110.7, 111.1, 111.3, 111.5, 111.8, 112.7, 113.2, 113.8, 114.3, 111.6],
        [102.8, 103.1, 103.6, 103.9, 104.5, 104.8, 105.2, 105.4, 106.1, 106.6, 106.9, 107.1, 105.0],
        [107.7, 108.3, 108.6, 108.9, 109.6, 110.2, 110.7, 111.3, 112.4, 113.9, 114.7, 115.0, 110.9],
        [116.4, 117.5, 118.5, 119.9, 121.6, 122.4, 123.0, 123.6, 124.2, 125.6, 127.0, 129.1, 122.4],
        [130.8, 133.0, 136.9, 138.6, 140.6, 143.3, 146.8, 149.8, 154.7, 157.9, 160.3, 161.7, 146.2],
        [163.6, 165.5, 165.7, 168.0, 169.1, 170.8, 171.8, 172.7, 174.3, 176.5, 178.0, 179.7, 171.3],
        [181.5, 184.5, 188.4, 194.0, 197.3, 198.2, 199.4, 201.1, 204.7, 211.6, 216.1, 218.8, 199.6],
        [110.0, 112.5, 114.2, 115.4, 116.9, 118.0, 118.9, 119.7, 121.0, 122.3, 124.1, 124.7, 118.1],
        [125.9, 127.2, 128.5, 129.9, 131.3, 132.4, 133.4, 134.0, 135.8, 137.3, 138.5, 139.5, 132.8],
        [142.2, 144.3, 146.1, 148.5, 150.4, 151.9, 153.3, 154.8, 158.6, 162.3, 164.4, 167.1, 153.7],
        [172.6, 175.6, 177.2, 180.0, 181.6, 183.3, 186.4, 188.3, 192.3, 195.6, 199.7, 202.3, 186.2],
        [110.1, 112.1, 113.7, 115.3, 116.9, 118.1, 119.1, 119.9, 121.6, 124.0, 126.1, 127.4, 118.7],
        [129.1, 130.8, 132.0, 133.2, 134.7, 136.0, 138.0, 140.5, 142.5, 145.3, 147.2, 148.2, 138.1],
        [150.3, 152.3, 153.7, 155.3, 156.8, 157.7, 159.2, 159.8, 161.9, 164.6, 166.3, 167.1, 158.8],
        [169.1, 170.9, 172.1, 173.3, 174.3, 175.3, 175.9, 176.4, 177.7, 179.5, 180.6, 181.8, 175.6],
        [183.7, 185.6, 186.9, 188.5, 189.6, 190.6, 191.2, 191.6, 192.4, 194.7, 196.1, 197.4, 190.7],
        [104.0, 104.7, 105.1, 105.4, 105.8, 106.2, 106.2, 106.4, 106.7, 107.3, 107.7, 108.0, 106.1],
        [108.7, 109.1, 109.5, 109.8, 110.2, 110.6, 110.9, 111.2, 112.0, 113.0, 113.3, 113.5, 111.0],
        [114.1, 114.4, 114.9, 115.3, 115.6, 116.0, 116.3, 116.8, 117.4, 118.3, 119.3, 119.7, 116.5],
        [120.6, 121.6, 122.2, 123.0, 123.5, 124.1, 124.4, 124.6, 125.2, 126.4, 126.9, 127.5, 124.2],
        [103.3, 104.0, 104.4, 104.8, 105.1, 105.5, 105.9, 106.6, 107.2, 108.1, 108.8, 109.2, 106.1],
        [110.0, 111.0, 111.3, 111.8, 112.2, 112.8, 113.0, 113.3, 113.8, 114.7, 115.5, 115.8, 112.9],
        [116.7, 116.9, 117.4, 117.9, 118.5, 118.9, 119.1, 119.2, 119.6, 120.3, 121.0, 121.2, 118.9],
        [102.3, 102.7, 102.9, 103.3, 103.7, 104.2, 104.6, 104.7, 104.8, 105.5, 106.0, 106.0, 104.2],
        [106.6, 107.0, 107.2, 107.5, 107.9, 108.1, 108.4, 108.6, 108.9, 109.5, 109.9, 110.3, 108.3],
        [110.7, 111.6, 112.5, 113.1, 113.8, 114.4, 114.5, 114.9, 115.2, 115.8, 116.5, 116.7, 114.1],
        [102.4, 102.7, 103.0, 103.6, 104.0, 104.2, 104.0, 104.1, 104.4, 104.5, 104.8, 104.9, 103.9],
        [105.1, 105.2, 105.3, 105.4, 105.7, 105.7, 105.7, 105.7, 105.9, 106.2, 106.5, 106.5, 105.7],
        [106.8, 107.1, 107.1, 107.3, 107.5, 107.6, 107.6, 107.7, 107.8, 108.0, 108.1, 108.1, 107.6],
        [108.2, 108.4, 108.6, 109.0, 109.2, 109.2, 109.4, 109.4, 109.7, 109.9, 110.3, 110.4, 109.3],
        [110.5, 111.0, 111.3, 111.4, 111.7, 112.1, 112.3, 112.3, 112.5, 112.8, 113.3, 113.4, 112.1],
        [113.9, 114.3, 114.4, 114.8, 115.1, 115.3, 115.3, 115.3, 115.4, 115.7, 115.9, 116.0, 115.1],
        [116.5, 116.9, 117.2, 117.5, 117.7, 117.9, 118.0, 118.2, 118.4, 118.7, 119.0, 119.1, 117.9],
        [119.6, 119.8, 120.2, 120.4, 120.5, 120.6, 120.9, 121.1, 121.4, 121.5, 121.8, 121.8, 120.8],
        [122.0, 122.4, 122.5, 122.8, 123.0, 123.3, 123.4, 123.6, 123.6, 123.6, 123.9, 123.9, 123.2],
        [123.9, 124.3, 124.5, 124.9, 125.1, 125.3, 125.6, 125.8, 125.9, 126.1, 126.1, 126.3, 125.3],
        [126.6, 126.9, 127.1, 127.4, 127.8, 127.9, 128.2, 128.4, 128.4, 128.2, 128.3, 128.4, 127.8],
        [128.5, 128.8, 129.0, 129.2, 129.6, 129.9, 130.2, 130.4, 130.4, 130.8, 131.3, 131.8, 130.0],
        [132.2, 132.5, 133.2, 133.5, 134.2, 134.8, 135.4, 135.5, 135.2, 135.2, 134.7, 134.5, 134.2],
        [134.2, 134.5, 134.5, 134.8, 135.1, 135.3, 135.3, 135.8, 135.4, 135.5, 135.6, 135.8, 135.2],
        [136.0, 136.2, 136.5, 137.0, 137.1, 137.1, 137.6, 137.9, 137.5, 137.8, 137.9, 138.4, 137.3],
        [101.2, 101.5, 101.9, 102.4, 102.5, 102.6, 102.9, 103.2, 103.2, 103.6, 103.7, 104.0, 102.7],
        [104.4, 104.8, 105.2, 105.7, 105.6, 105.8, 105.9, 106.4, 106.4, 106.4, 106.2, 106.5, 105.8],
        [106.7, 106.7, 106.9, 106.9, 106.9, 107.1, 107.2, 107.6, 107.2, 107.1, 106.8, 107.1, 107.0],
        [107.3, 107.2, 107.2, 107.4, 107.3, 107.4, 107.3, 107.5, 107.1, 107.2, 107.0, 107.0, 107.2],
        [106.5, 106.8, 107.0, 107.1, 107.2, 107.3, 107.2, 107.4, 107.0, 107.2, 107.0, 107.0, 107.1],
        [ 99.7,  99.5,  99.6,  99.6,  99.7,  99.9, 100.0, 100.2, 100.0, 100.0, 100.0, 100.3, 99.9],
        [100.6, 101.0, 101.0, 101.3, 101.1, 101.0, 101.0, 101.4, 101.1, 100.9, 100.8, 101.1, 101.0],
        [101.5, 101.5, 101.7, 101.7, 102.0, 102.2, 102.5, 102.9, 102.4, 102.4, 102.2, 102.1, 102.1],
        [102.2, 102.3, 102.5, 102.6, 102.7, 102.7, 102.7, 103.2, 102.5, 102.4, 102.3, 102.5, 102.6],
        [102.7, 102.5, 102.6, 102.5, 102.3, 102.4, 102.3, 102.5, 101.9, 102.0, 102.0, 102.3, 102.3],
        [102.9, 103.0, 103.3, 103.7, 103.6, 103.8, 104.2, 104.7, 104.5, 105.1, 105.7, 106.2, 104.2],
        [107.7, 108.8, 109.9, 109.7, 110.6, 111.9, 112.3, 113.2, 113.5, 117.2, 117.9, 118.2, 112.6],
        [118.3, 118.5, 118.0, 118.4, 118.6, 118.6, 118.7, 119.1, 118.3,   0.0,   0.0,   0.0,   0.0]];
    
    aidx[usize::try_from(yyyy - 1947).unwrap()][usize::try_from(mm - 1).unwrap()]
}

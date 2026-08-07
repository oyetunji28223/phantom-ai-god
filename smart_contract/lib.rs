#[macro_export]
macro_rules! msg {
    ($($arg:tt)*) => {
        #[cfg(target_arch = "bpf")]
        solana_program::log::sol_log(&format!($($arg)*));
        #[cfg(not(target_arch = "bpf"))]
        println!($($arg)*);
    };
}

pub fn execute_trade() {
    msg!("Trade executed.");
}

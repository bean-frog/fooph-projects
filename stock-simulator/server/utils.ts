class Utils {
	// logging
		// ansi codes
	public static readonly RED = '\x1b[31m';
	public static readonly GREEN = '\x1b[32m';
	public static readonly WHITE = '\x1b[37m';
	public static readonly YELLOW = '\x1b[33m';
	public static readonly BOLD = '\x1b[1m';
	public static readonly RESET = '\x1b[0m'; 
		// funcs
	public static success(message: string): void {
		console.log(`${this.BOLD}${this.WHITE}[${this.RESET}${this.BOLD}${this.GREEN}Success${this.RESET}${this.BOLD}${this.WHITE}]:${this.RESET} ${message}`)
	}
	public static warning(message: string): void {
		console.warn(`${this.BOLD}${this.WHITE}[${this.RESET}${this.BOLD}${this.YELLOW}Warning${this.RESET}${this.BOLD}${this.WHITE}]:${this.RESET} ${message}`)
	}
	public static failure(message: string): void {
		console.error(`${this.BOLD}${this.WHITE}[${this.RESET}${this.BOLD}${this.RED}Failure${this.RESET}${this.BOLD}${this.WHITE}]:${this.RESET} ${message}`)
	}
	public static info(message:string): void {
		console.log(`${this.BOLD}${this.WHITE}[Info]:${this.RESET}${message}`)
	}

} // Utils
export default Utils

public class StepTracker {
	private int days = 0;
	private int daysActive = 0;
	private int threshold;
	private int steps = 0;
	public StepTracker(int threshold) {
		this.threshold = threshold;
	}
	public StepTracker() {
		this.threshold = 10000;
	}
	public int activeDays() {
		return daysActive;
	}
	public double averageSteps() {
		if (this.steps != 0) {
			return (double)this.steps / (double)this.days;
		} else {
			return 0.0;
		}
	}
	public void addDailySteps(int steps) {
		this.days++;
		if (steps >= this.threshold) {
			this.daysActive++;
		}
		this.steps += steps;
	}
	
}

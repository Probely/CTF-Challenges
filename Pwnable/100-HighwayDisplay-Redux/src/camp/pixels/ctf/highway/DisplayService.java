package camp.pixels.ctf.highway;

public class DisplayService {
	private Display display = new Display();

	public Display getDisplay() {
		return this.display;
	}

	public void setText(Display d) {
		this.display = d;
	}

}

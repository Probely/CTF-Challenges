package camp.pixels.ctf.highway;

import java.io.Serializable;

public class Display implements Serializable {
	private static final long serialVersionUID = 7630566514436928811L;
	private static final String DEFAULT_MESSAGE = "--testing--";
	private String message = DEFAULT_MESSAGE;
	
	public String getMessage() {
		return this.message;
	}
	
	public void setMessage(String msg) {
		this.message = msg;
	}
}

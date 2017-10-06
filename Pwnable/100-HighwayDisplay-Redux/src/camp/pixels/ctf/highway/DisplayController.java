package camp.pixels.ctf.highway;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.Base64;
import org.apache.commons.lang3.SerializationUtils;

import static spark.Spark.*;

public class DisplayController {

	public DisplayController(final DisplayService srv, int listen) {

		if (listen > 0 && listen < 65536) {
			port(listen);
		}

		get("/text", (req, res) -> {
			byte[] data = SerializationUtils.serialize(srv.getDisplay());
			return Base64.getEncoder().encodeToString(data);
		});

		post("/text", (req, res) -> {
			String body = req.body();
			body = body.replace("\n", "").replace("\r\n", "");
			System.out.println("Got request: [" + body + "]");
			byte[] data = Base64.getDecoder().decode(body);
			Display d = SerializationUtils.deserialize(data);
			srv.setText(d);
			return "Message updated!";
		});

		exception(IllegalArgumentException.class, (e, req, res) -> {
			res.status(400);
			res.body(e.getMessage());
		});

		exception(Exception.class, (e, req, res) -> {
			StringWriter buffer = new StringWriter();
			PrintWriter printer = new PrintWriter(buffer);
			e.printStackTrace(printer);
			res.status(500);
			res.body(buffer.toString());
		});

		notFound((req, res) -> {
		    return "Not found.";
		});		
		after((req, res) -> {
			res.type("text/plain");
		});

	}
}
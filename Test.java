import okhttp-3.9.0.MediaType;
import okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;
import com.squareup.okhttp.Response;
 class OkHttpClient {
    public static void main(String[] args) {
    OkHttpClient client = new OkHttpClient().newBuilder();
    MediaType mediaType = MediaType.parse("application/json");
    RequestBody body = RequestBody.create(mediaType, "{\n \"text\": \"string\",\n \"tar_lan\": \"hi\",\n \"src_lan\": \"en\"\n}");
    Request request = new Request.Builder();
    .url("https://panini.nic.in:8121/translation")
    .method("POST", body)
    .addHeader("accept", "application/json")
    .addHeader("Content-Type", "application/json")
    .build();
    Response response = client.newCall(request).execute();
    }
}
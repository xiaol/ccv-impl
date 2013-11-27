package nlp;

import py4j.GatewayServer;
import edu.fudan.ml.types.Dictionary;
import org.fnlp.app.keyword.AbstractExtractor;
import org.fnlp.app.keyword.WordExtract;

import edu.fudan.nlp.cn.tag.CWSTagger;
import edu.fudan.nlp.corpus.StopWords;
import java.util.Map;


// java -classpath .:../../env/share/py4j/py4j0.8.jar:fudannlp.jar:lib/commons-cli-1.2.jar:lib/trove.jar nlp.NLPEntryPoint
// java -classpath .:/usr/local/python2.7/lib/python2.7/site-packages/py4j-0.8-py2.7.egg/share/py4j/py4j0.8.jar:fudannlp.jar:lib/commons-cli-1.2.jar:lib/trove.jar nlp.NLPEntryPoint
public class NLPEntryPoint {
    private static StopWords sw = null;
    private static CWSTagger seg = null;
    private static AbstractExtractor key = null;

    public NLPEntryPoint() {
        
    }

    public static void init() throws Exception{
        if(sw == null || seg == null || key == null){
            sw= new StopWords("models/stopwords");
            seg = new CWSTagger("models/seg.m");
            key = new WordExtract(seg,sw); 
        }
    }

    public static String extractKeywords(String sentencs, int num, boolean isWeighted) throws Exception{
        init();
        Map<String,Integer> keywordsMap =  key.extract(sentencs,num);
        String result = "";
        int count = 0;
        for(Map.Entry<String, Integer> entry : keywordsMap.entrySet()){
            if(count == 0)
                result = entry.getKey();
            else
                result += " " + entry.getKey();
            count++;
        }
        return result;
    }

    public static void main(String[] args) throws Exception{
        GatewayServer gatewayServer = new GatewayServer(new NLPEntryPoint());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }

}
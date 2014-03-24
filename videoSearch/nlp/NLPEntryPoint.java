package nlp;

import py4j.GatewayServer;
import edu.fudan.ml.types.Dictionary;
import org.fnlp.app.keyword.AbstractExtractor;
import org.fnlp.app.keyword.WordExtract;

import edu.fudan.nlp.cn.tag.CWSTagger;
import edu.fudan.nlp.corpus.StopWords;
import edu.fudan.nlp.cn.tag.POSTagger;
import java.util.Map;
import edu.fudan.nlp.cn.tag.NERTagger;

import java.util.HashMap;

// java -classpath .:../../env/share/py4j/py4j0.8.jar:fudannlp.jar:lib/commons-cli-1.2.jar:lib/trove.jar nlp.NLPEntryPoint
// java -classpath .:/usr/local/python2.7/lib/python2.7/site-packages/py4j-0.8-py2.7.egg/share/py4j/py4j0.8.jar:fudannlp.jar:lib/commons-cli-1.2.jar:lib/trove.jar nlp.NLPEntryPoint
public class NLPEntryPoint {
    private static StopWords sw = null;
    private static CWSTagger seg = null;
    private static AbstractExtractor key = null;
    private static POSTagger tag = null;
    private static NERTagger  nerTag = null;

    public NLPEntryPoint() {
        
    }

    public static void init() throws Exception{
        if(sw == null || seg == null || key == null || tag == null){
            sw= new StopWords("models/stopwords");
            seg = new CWSTagger("models/seg.m",new Dictionary("models/dict.txt"));
            key = new WordExtract(seg,sw);
            tag = new POSTagger("models/pos.m");
            nerTag = new NERTagger("./models/seg.m","./models/pos.m");
        }
    }

    public static String extractKeywords(String sentencs, int num, boolean isWeighted) throws Exception{
        init();
        Map<String,Integer> keywordsMap =  key.extract(sentencs,num);
        String result = "";
        int count = 0;

        String[] keys = keywordsMap.keySet().toArray(new String[0]);
        String[] s1 = tag.tagSeged(keys);
        for(int i = 0; i < s1.length; i++){
             if(s1[i].equals("副词") || s1[i].equals("形容词") || 
                    s1[i].equals("动词") || s1[i].equals("数词") || s1[i].equals("序数词") 
                    || s1[i].equals("表情符") || s1[i].equals("限定词")|| s1[i].equals("介词") || s1[i].equals("指示代词")){
             }else{
                System.out.print(keys[i]+"/"+s1[i]+" ");
                if(count == 0){
                    result = keys[i];
                    count ++;
                }else
                    result += " " + keys[i];
             }
        }
        return result;
    }

    public static boolean POS(String tags) throws Exception{
            init();
            String[] keys = tags.split(" ");
            String[] s1 = tag.tagSeged(keys);
            for(int i = 0; i < s1.length; i++){
                if(s1[i].equals("副词") || s1[i].equals("形容词") || 
                    s1[i].equals("动词") || s1[i].equals("数词") || s1[i].equals("序数词") 
                    || s1[i].equals("表情符") || s1[i].equals("限定词")|| s1[i].equals("介词") || s1[i].equals("指示代词")
                     || s1[i].equals("时间短语") ){
                }else{
                    System.out.print(keys[i]+"/"+s1[i]+" ");
                    return true;
                }
            }
            return false;
        }

    public static HashMap<String, String> NERTag(String sentence) throws Exception{
           init();
           HashMap<String, String> map = new HashMap<String, String>();
           nerTag.tag(sentence,map);
           return map;
    }

    public static void main(String[] args) throws Exception{
        GatewayServer gatewayServer = new GatewayServer(new NLPEntryPoint());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }
}
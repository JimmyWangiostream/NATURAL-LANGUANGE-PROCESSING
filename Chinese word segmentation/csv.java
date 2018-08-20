
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Array;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.StringTokenizer;
import java.util.Scanner;
public class csv {
	public static void main(String[] args) {
		try {
			
			String doc=".";
			String tmp;
			String t;
			String parse=null;
			String[] dic= new String[200000];
			//String article="商業大亨川普明年將成為美國總統";
			String article="馬祖及西半部地區易有局部霧或低雲影響能見度";
			System.out.println("輸入: "+article);
			int len=article.length();
			String answer="";
			int ans=0;
			int change=0;
			int index=0;
			int find=0;
			String strLine;
			FileReader fr;
            BufferedReader brdFile;
			int remain=len;//length of article after parse 
			fr = new FileReader("C:\\dict_revised_2015_20160523_1.csv");//抓CSV檔進java
            brdFile = new BufferedReader(fr);//bufferedReader
            strLine = null;
            while((strLine = brdFile.readLine())!=null){//將CSV檔字串一列一列讀入並存起來直到沒有列為止
            	StringTokenizer st = new StringTokenizer(strLine, ",");
            	
            	tmp=st.nextToken();
            	if(tmp.length()>3)
            	{
            		t=(String) tmp.subSequence(1,2);
            		if(t.compareTo(doc)==0)
            		{
            			continue;
            		}
            	}
            	if(st.hasMoreTokens())
            		st.nextToken();
            	if(st.hasMoreTokens())
            		dic[index]=st.nextToken();
                ans++;
                index++;
            	
			}
            
            fr = new FileReader("C:\\dict_revised_2015_20160523_2.csv");//抓CSV檔進java
            brdFile = new BufferedReader(fr);//bufferedReader
            strLine = null;
            while((strLine = brdFile.readLine())!=null){//將CSV檔字串一列一列讀入並存起來直到沒有列為止
            	StringTokenizer st = new StringTokenizer(strLine, ",");
            	
            	tmp=st.nextToken();
            	if(tmp.length()>3)
            	{
            		t=(String) tmp.subSequence(1,2);
            		if(t.compareTo(doc)==0)
            		{
            			continue;
            		}
            	}
            	if(st.hasMoreTokens())
            		st.nextToken();
            	if(st.hasMoreTokens())
            		dic[index]=st.nextToken();
                ans++;
                index++;
            	
			}
            
            fr = new FileReader("C:\\dict_revised_2015_20160523_3.csv");//抓CSV檔進java
            brdFile = new BufferedReader(fr);//bufferedReader
            strLine = null;
            while((strLine = brdFile.readLine())!=null){//將CSV檔字串一列一列讀入並存起來直到沒有列為止
            	StringTokenizer st = new StringTokenizer(strLine, ",");
            	
            	tmp=st.nextToken();
            	if(tmp.length()>3)
            	{
            		t=(String) tmp.subSequence(1,2);
            		if(t.compareTo(doc)==0)
            		{
            			continue;
            		}
            	}
            	if(st.hasMoreTokens())
            		st.nextToken();
            	if(st.hasMoreTokens())
            		dic[index]=st.nextToken();
                ans++;
                index++;
            	
			}
          


			while(remain>0) 
			{
				for(int i=59;i>1;i--)
				{
					change=0;
					if(remain<i) continue;
						parse=(String) article.subSequence(find,find+i);
						//System.out.println(parse+i);
					for(int j=0;j<index-1;j++)
					{	
						if(parse.length()>0) 
						{
						if(parse.equals(dic[j]))
						{
							answer += (parse+"  ");
							find+=i;
							remain=len-find;
							//System.out.println(parse+" "+len+" "+remain+" "+find);
							change=1;							
							break;
						}
						
						}	
				
					}
					if(change==1) 
					{
						break;
					}
				}
				
				if(find<len&&change==0)
				{
					answer += ((String) article.subSequence(find,find+1)+"  ");
					//System.out.println(parse);
					find++;
					remain--;
				}				
			}
			
			//System.out.println(a);
			System.out.println("輸出: "+answer);
		}catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}catch (IOException e) {
				// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}


	
}
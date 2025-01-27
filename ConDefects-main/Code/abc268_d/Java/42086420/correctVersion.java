import java.io.*;
import java.lang.reflect.Array;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;
import java.util.function.*;
import java.util.stream.*;
import java.awt.Point;

import static java.lang.Math.*;
import static java.util.Arrays.*;
import static java.util.Collections.*;
import static java.util.Comparator.*;

class Solver{
  static int infI = (int) 1e9;
  static long infL = (long) 1e18;
  static long mod = (int) 1e9 +7;
  //  static long mod = 998244353;
  static String yes = "Yes";
  static String no = "No";

  Util util = new Util();
  Random rd = ThreadLocalRandom.current();
  MyReader in = new MyReader(System.in);
  MyWriter out = new MyWriter(System.out);
  MyWriter log = new MyWriter(System.err){
    @Override
    protected void ln(){
      super.ln();
      flush();
    };
  };

  int N = in.it();
  int M = in.it();

  String[] S = in.str(N);
  String[] T = in.str(M);

  Set<String> ngs = new HashSet<>();

  Object solve(){
    Collections.addAll(ngs,T);

    int n = 16 -(N -1);
    for (var s:S)
      n -= s.length();

    var pm = new Permutation(N);

    do {
      String ans = dfs(1,S[pm.arr[0]],pm,n);
      if (ans != null)
        return ans;
    } while (pm.increment());
    return -1;
  }

  private String dfs(int i,String str,Permutation pm,int n){
    if (i == N)
      return ngs.contains(str) || str.length() < 3 ? null : str;

    for (int k = 0;k <= n;k++) {
      var tmp = dfs(i +1,str +"_" +"_".repeat(k) +S[pm.arr[i]],pm,n -k);
      if (tmp != null)
        return tmp;
    }

    return null;
  }

  boolean valid(int i,int N){ return 0 <= i && i < N; }

  int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
}

class Permutation{
  int n;
  int[] arr;
  int[] fac;

  Permutation(int n){
    this.n = n;
    arr = new int[n];
    Arrays.setAll(arr,i -> i);
    fac = new int[n];
    fac[0] = 1;
    for (int i = 1;i < n;i++)
      fac[i] = i *fac[i -1];
  }

  boolean increment(){
    int l = n -2;
    while (0 <= l && arr[l] > arr[l +1])
      l--;

    if (l < 0)
      return false;

    int r = n -1;
    while (arr[l] > arr[r])
      r--;

    swap(l,r);

    l++;
    r = n -1;
    while (l < r)
      swap(l++,r--);

    return true;
  }

  void swap(int l,int r){
    arr[l] ^= arr[r];
    arr[r] ^= arr[l];
    arr[l] ^= arr[r];
  }

}

class Edge{
  int id;
  int u;
  int v;
  long l;
  Edge rev;

  Edge(int id,int u,int v){
    this.id = id;
    this.u = u;
    this.v = v;
  }

  void rev(Edge rev){ rev.l = l; }

}

class Util{
  long st = System.currentTimeMillis();

  long elapsed(){ return System.currentTimeMillis() -st; }

  static void reverse(Object arr){
    if (!arr.getClass().isArray())
      throw new UnsupportedOperationException("reverse");

    int l = 0;
    int r = Array.getLength(arr) -1;

    while (l < r) {
      Object t = Array.get(arr,l);
      Array.set(arr,l,Array.get(arr,r));
      Array.set(arr,r,t);
      l++;
      r--;
    }

  }

  static int[][] trans(int[]... T){ return arr(new int[T[0].length][],i -> arrI(T.length,j -> T[j][i])); }

  static int[][] addId(int[][] T){
    return arr(new int[T.length][],i -> {
      int[] t = copyOf(T[i],T[i].length +1);
      t[t.length -1] = i;
      return t;
    });
  }

  static long[][] trans(long[]... T){ return arr(new long[T[0].length][],i -> arrL(T.length,j -> T[j][i])); }

  static double[][] trans(double[]... T){ return arr(new double[T[0].length][],i -> arrD(T.length,j -> T[j][i])); }

  static int[] arrI(int N,IntUnaryOperator f){
    int[] ret = new int[N];
    setAll(ret,f);
    return ret;
  }

  static long[] arrL(int N,IntToLongFunction f){
    long[] ret = new long[N];
    setAll(ret,f);
    return ret;
  }

  static double[] arrD(int N,IntToDoubleFunction f){
    double[] ret = new double[N];
    setAll(ret,f);
    return ret;
  }

  static <T> T[] arr(T[] arr,IntFunction<T> f){
    setAll(arr,f);
    return arr;
  }

}

class MyReader{
  byte[] buf = new byte[1 <<16];
  int ptr = 0;
  int tail = 0;
  InputStream in;

  MyReader(InputStream in){ this.in = in; }

  byte read(){
    if (ptr == tail)
      try {
        tail = in.read(buf);
        ptr = 0;
      } catch (IOException e) {}
    return buf[ptr++];
  }

  boolean isPrintable(byte c){ return 32 < c && c < 127; }

  boolean isNum(byte c){ return 47 < c && c < 58; }

  byte nextPrintable(){
    byte ret = read();
    while (!isPrintable(ret))
      ret = read();
    return ret;
  }

  int it(){ return Math.toIntExact(lg()); }

  int[] it(int N){ return Util.arrI(N,i -> it()); }

  int[][] it(int H,int W){ return Util.arr(new int[H][],i -> it(W)); }

  int idx(){ return it() -1; }

  int[] idx(int N){ return Util.arrI(N,i -> idx()); }

  int[][] idx(int H,int W){ return Util.arr(new int[H][],i -> idx(W)); }

  int[][] qry(int Q){ return Util.arr(new int[Q][],i -> new int[]{idx(), idx(), i}); }

  long lg(){
    byte i = nextPrintable();
    boolean negative = i == 45;
    long n = negative ? 0 : i -'0';
    while (isPrintable(i = read()))
      n = 10 *n +i -'0';
    return negative ? -n : n;
  }

  long[] lg(int N){ return Util.arrL(N,i -> lg()); }

  long[][] lg(int H,int W){ return Util.arr(new long[H][],i -> lg(W)); }

  double dbl(){ return Double.parseDouble(str()); }

  double[] dbl(int N){ return Util.arrD(N,i -> dbl()); }

  double[][] dbl(int H,int W){ return Util.arr(new double[H][],i -> dbl(W)); }

  char[] ch(){ return str().toCharArray(); }

  char[][] ch(int H){ return Util.arr(new char[H][],i -> ch()); }

  String line(){
    StringBuilder sb = new StringBuilder();

    for (byte c;(c = read()) != '\n';)
      sb.append((char) c);
    return sb.toString();
  }

  String str(){
    StringBuilder sb = new StringBuilder();
    sb.append((char) nextPrintable());

    for (byte c;isPrintable(c = read());)
      sb.append((char) c);
    return sb.toString();
  }

  String[] str(int N){ return Util.arr(new String[N],i -> str()); }

  Edge[] e(int N,int M){ return e(N,M,e -> e.l = 1); }

  Edge[] e(int N,int M,Consumer<Edge> f){
    return Util.arr(new Edge[M],i -> {
      Edge e = new Edge(i,idx(),idx());
      f.accept(e);
      return e;
    });
  }

  Edge[][] g(int N,int M,boolean b){ return g(N,b,e(N,M)); }

  Edge[][] g(int N,int M,boolean b,Consumer<Edge> f){ return g(N,b,e(N,M,f)); }

  Edge[][] g(int N,boolean b,Edge[] E){
    int[] c = new int[N];

    for (Edge e:E) {
      c[e.u]++;
      if (!b)
        c[e.v]++;
    }

    Edge[][] g = Util.arr(new Edge[N][],i -> new Edge[c[i]]);

    for (Edge e:E) {

      g[e.u][--c[e.u]] = e;
      if (!b) {
        Edge rev = new Edge(e.id,e.v,e.u);
        e.rev(rev);
        g[e.v][--c[e.v]] = e.rev = rev;
      }
    }
    return g;
  }
}

class MyWriter{
  OutputStream out;
  byte[] buf = new byte[1 <<16];
  byte[] ibuf = new byte[20];
  int tail = 0;

  MyWriter(OutputStream out){ this.out = out; }

  void flush(){
    try {
      out.write(buf,0,tail);
      tail = 0;
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  protected void ln(){ write((byte) '\n'); }

  private void write(byte b){
    buf[tail++] = b;
    if (tail == buf.length)
      flush();
  }

  private void write(byte[] b,int off,int len){
    for (int i = off;i < off +len;i++)
      write(b[i]);
  }

  private void write(long n){
    if (n < 0) {
      n = -n;
      write((byte) '-');
    }

    int i = ibuf.length;
    do {
      ibuf[--i] = (byte) (n %10 +'0');
      n /= 10;
    } while (n > 0);

    write(ibuf,i,ibuf.length -i);
  }

  private void print(Object obj){
    if (obj instanceof Boolean)
      print((boolean) obj ? Solver.yes : Solver.no);
    else if (obj instanceof Character)
      write((byte) (char) obj);
    else if (obj instanceof Integer)
      write((int) obj);
    else if (obj instanceof Long)
      write((long) obj);
    else if (obj instanceof char[])
      for (char b:(char[]) obj)
        write((byte) b);
    else if (obj instanceof Collection<?>) {
      Iterator<?> itr = ((Collection<?>) obj).iterator();
      while (itr.hasNext()) {
        print(itr.next());
        if (itr.hasNext())
          ln();
      }
    } else if (obj.getClass().isArray()) {
      int l = Array.getLength(obj);
      boolean ln = false;

      if (0 < l) {
        Object a = Array.get(obj,0);
        ln = !(a instanceof char[]) && a.getClass().isArray();
      }
      for (int i = 0;i +1 < l;i++) {
        print(Array.get(obj,i));
        write((byte) (ln ? '\n' : ' '));
      }
      print(Array.get(obj,l -1));
    } else
      for (char b:Objects.toString(obj).toCharArray())
        write((byte) b);
  }

  void println(Object obj){
    if (obj == null)
      return;
    print(obj);
    ln();
  }
}

class Main{
  public static void main(String[] args) throws Exception{
    Solver solver = new Solver();
    Optional.ofNullable(solver.solve()).ifPresent(solver.out::println);
    solver.out.flush();
    solver.log.println(solver.util.elapsed());
  }
}
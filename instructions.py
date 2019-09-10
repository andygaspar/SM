"""
    #calcolo distanza da areoporto *********************************
    AIRPORT=(50.03793, 8.56215)
    dist=geodesic(ENTRY,AIRPORT).kilometers
    dist



    # rielaborazione stringhe ****************************************
    df_wp.head(100)
    type(df_wp["coor"][2])
    test=df_wp["coor"][2]
    test
    test=test.replace("POINT","")
    test=test.replace("(","")
    test=test.replace(")","")
    test
    split_test=test.split(" ")
    split_test
    split_test=[float(split_test[0]),float(split_test[1])]
    split_test=tuple(split_test)
    split_test



    #creare data frame ************************************************

    t=["ciccio","pasticcio"]          #stringa dei nomi
    dati=[[1],[2]]                    #dati: ATTENZIONE!! non valori numerici....in caso liste con un solo valore
    di=dict(zip(t,dati))              #dizionario con i dati e gli stessi nomi di pippo
    df=pd.DataFrame(di)                #nuovo dataframe da dict
    df

    #versione compatta
    df=pd.DataFrame(dict(zip(t,dati)))
    df



    # *********************************************************

    dati=["zio", [[1,2,3]]]
    di=dict(zip(t,dati))        #dizionario con i dati e gli stessi nomi di df
    o=pd.DataFrame(di)          #nuovo dataframe da dict
    df=df.append(o)             #append finale  (vedere sotto indicazioni dul index!!!!!!)
    df

    #versione compatta
    dati=["zio", [[1,2,3]]]
    df.append(pd.DataFrame(dict(zip(t,dati))))


    #append di righe (altra spiegazione da internet ) ***************************************************************
    df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
    df
       A  B
    0  1  2
    1  3  4

    df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
    df.append(df2)
       A  B
    0  1  2
    1  3  4
    0  5  6
    1  7  8



    Importante!!!: ignore_index=True:   non eredita gli indici riga ma li ordina
    df.append(df2, ignore_index=True)
       A  B
    0  1  2
    1  3  4
    2  5  6
    3  7  8




    #ricerca per caratteristtica, crea oggetto true false che può essere letto da df ***************************************
    ar_1=df_ar['ifps_id']=="AA66960337"

    #df da oggetto true false
    ar_fl_1=df_ar[ar_1]
    ar_fl_1




    #crea una una colonna dal nome "distance" e assegna il vettore,lista..wp_dist ***********************
    df_wp["distance"]=wp_dist




    #come esportare un csv da un df **********************************************************************
    export_csv = df_entry.to_csv (r'../data/df_entry.csv', index = None, header=True)



    #size del dataframe ***************************************************************
    df_wp.shape



    # accedere righe, colonne, elementi di un df per indice *****************************************
    df.iloc[i]                          i-esima riga del df
    df.iloc[i,j] = df.iloc[i][j]        elemento i,j
    df.iloc[:,j]                        j-esima colonna

    df.iloc[i]["CODICE FISCALE"]        i-esima riga, label="CODICE FISCSLE"
    df.iloc[:]["CODICE FISCALE"]        tutti i COD FISCALI(colonna)




    #accedere e assegnare nomi alle colonne  ********************************************************
    list(df.columns)                                        lista con i nomi
    df.columns =['Col_1', 'Col_2']                          assegna o cambia nome colonne
    df.index = ['Row_1', 'Row_2', 'Row_3', 'Row_4']         asseggna o cambia nome righe
    df = df.rename(columns = {"Col_1":"Mod_col"})           cambia specifico nome colonne
    df = df.rename({"Mod_col":"Col_1","B":"Col_2"}, axis='columns')     cambia specifici nomi colonne, multipli















"""

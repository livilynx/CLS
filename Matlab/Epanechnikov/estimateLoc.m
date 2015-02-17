function mat = estimateLoc(diagFile);


addpath('..\Utilities');
addpath('..\RWFormats');
addpath('..\ModLuth');

[res, balise, reference, iniMatrix] = readDiag (diagFile);

mat = ReadAllDiag(diagFile);



col_lc = 3;
col_lat1 = 5 ;
col_lon1 = 6 ;
col_lat2 = 7;
col_lon2 = 8;

col_flag = 9;
iniMatrix(:,col_flag) = 0;
%iniMatrix = detecter_doublons(iniMatrix); 
%iniMatrix = correction_mat_choix_loc(iniMatrix);

iniMatrix(:,col_flag) = 0;


iniMatrix(find(iniMatrix(:,col_lat1) == 9999),col_lc) = -10;
iniMatrix(find(iniMatrix(:,col_lon1) == 9999),col_lc) = -10;

demi_fen_min1 = 43200;
demi_fen_max1 = 86400;
nb_pt_demi_fenetre_estim1 = 2;
min_estim1 = 2;

estim1 = z_estimation(iniMatrix);

ind = (find(estim1(:,2) ==9999 | estim1(:,3) ==9999 ));
ind(find(ind==1)) = [];
ind(find(ind==size(estim1,1))) = [];

for (i=1:length(ind)) 
     j = ind(i);
     ind_prev = max(find(estim1(1:j,2)<9999));
     ind_next = j + min(find(estim1(j+1:end,2)<9999));
   
     if (isempty(ind_prev)); continue; end;
     if (isempty(ind_next)); continue; end;  
     
     estim1(j,2) = estim1(ind_prev,2) + (estim1(ind_next,2)-estim1(ind_prev,2))* (estim1(j,1)-estim1(ind_prev,1))/(estim1(ind_next,1)-estim1(ind_prev,1));
     estim1(j,3) = estim1(ind_prev,3) + (estim1(ind_next,3)-estim1(ind_prev,3))* (estim1(j,1)-estim1(ind_prev,1))/(estim1(ind_next,1)-estim1(ind_prev,1));
end
    
iniMatrix(find(iniMatrix(:,col_lc)== -10), col_lat1) = estim1 (find(iniMatrix(:,col_lc)== -10), 2);
iniMatrix(find(iniMatrix(:,col_lc)== -10), col_lon1) = estim1 (find(iniMatrix(:,col_lc)== -10), 3);
iniMatrix(find(iniMatrix(:,col_lc)== -10), col_lat2) = estim1 (find(iniMatrix(:,col_lc)== -10), 2);
iniMatrix(find(iniMatrix(:,col_lc)== -10), col_lon2) = estim1 (find(iniMatrix(:,col_lc)== -10), 3);


mat (:,4) = iniMatrix(:,col_lc);
mat (:, 6:9) = iniMatrix(:,col_lat1:col_lon2);

return;